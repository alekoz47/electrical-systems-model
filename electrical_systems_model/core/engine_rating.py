import time

import pandas as pd
from scipy.optimize import minimize
from scipy.optimize import basinhopping

from core.engine_loading import EngineLoadSelector


class EngineRatingSelector:
    def __init__(self, source_list, load_cases):
        self.source_list = source_list
        self.load_cases = load_cases
        self.bounds = []
        self.constraints = []
        self.result = None
        self.old_engine_loading = [[0] * 2 * len(source_list)] * len(load_cases)
        self.previous_iterate_time = None
        self.iteration_time = None

        self.columns = []
        self.set_columns()
        self.opti_data = pd.DataFrame(columns=self.columns)

        self.optimize_engine_ratings()
        # self.basin_hopper()

        self.write_to_csv()

    def optimize_engine_ratings(self):
        # self.set_constraints()
        self.optimizer()

    def set_constraints(self):
        # TODO: make this an inequality constraint to allow for float error
        # Something different for shaft power?

        for index, source in enumerate(self.source_list):
            def non_zero_constraint(engine_loading):
                return self.power_brake - self.power

            self.constraints.append({
                'type': 'ineq',
                'fun': non_zero_constraint
            })

    def set_columns(self):

        ratings_name_list = []
        loadings_name_list = []
        fuel_burn_list = []

        self.source_list = sorted(self.source_list, key=lambda x: str(type(x)))
        types = map(type, self.source_list)
        types = set(types)
        types = list(types)

        for type_i in types:
            sub_list = list(filter(lambda x: type(x) is type_i, self.source_list))
            for index, source in enumerate(sub_list):
                ratings_name_list.append(source.type_name() + ' ' + str(index + 1))
            for case in self.load_cases:
                for index, source in enumerate(sub_list):
                    loadings_name_list.append(
                        source.type_name() + ' ' + str(index + 1) + ': ' + case['Name'] + ' Mechanical Loading')
                    loadings_name_list.append(
                        source.type_name() + ' ' + str(index + 1) + ': ' + case['Name'] + ' Electrical Loading')

        for case in self.load_cases:
            fuel_burn_list.append(case['Name'] + ' Fuel Burn Rate')

        self.columns.extend(ratings_name_list)
        self.columns.extend(loadings_name_list)
        self.columns.extend(fuel_burn_list)
        self.columns.append('Iteration Time')
        print(self.columns)

    def write_to_csv(self):
        self.opti_data.to_csv('../../tests/outputs/output.csv', index_label=True)

    def obj_func(self, engine_rating, source_list, load_cases):
        if self.previous_iterate_time is not None:
            self.iteration_time = time.time() - self.previous_iterate_time
            print('Iteration Time: ', round(self.iteration_time, 2))

        self.previous_iterate_time = time.time()

        normalized_fuel_burn = 0
        new_engine_loading = []

        for index, source in enumerate(source_list):
            source.power_brake = engine_rating[index]

        fuel_burn_list = []

        # for loop for each operating case
        for index, case in enumerate(load_cases):
            mechanical_power = case['Mechanical Power']
            electrical_power = case['Electrical Power']
            case_percent = case['Use Factor']

            # Make initial guess of loading the previous iterations optimized loadings

            load_case_optimizer = EngineLoadSelector(source_list, mechanical_power, electrical_power,
                                                     self.old_engine_loading[index])
            case_fuel_burn = load_case_optimizer.result.fun
            normalized_fuel_burn += case_percent * case_fuel_burn
            fuel_burn_list.append(case_percent * case_fuel_burn)

            new_engine_loading.append(load_case_optimizer.result.x)

        print('Engine Ratings:', engine_rating)
        print('Engine Loading:', new_engine_loading)
        print('Normalized Fuel Burn (MT/hr):', normalized_fuel_burn)
        print()

        data_list = []
        data_list.extend(engine_rating)
        for case in self.old_engine_loading:
            data_list.extend(case)

        data_list.extend(fuel_burn_list)
        data_list.append(self.iteration_time)

        print(data_list)
        if self.iteration_time is not None:
            data_list_pd = pd.DataFrame([data_list], columns=self.columns)
            self.opti_data = self.opti_data.append(data_list_pd, ignore_index=True)

        self.old_engine_loading = new_engine_loading

        return normalized_fuel_burn

    def optimizer(self):
        self.result = minimize(
            fun=self.obj_func,
            args=(self.source_list, self.load_cases),
            # x0=[1500]*len(self.source_list),
            x0=[2000, 1000, 1],
            # bounds=[(0, 5000)]*len(self.source_list),
            # constraints = self.constraints,
            method='L-BFGS-B',
            options={'gtol': 1e-09}
            # options = {'maxiter': 100, 'ftol': 1e-11} # 'eps': 10
        )

    def basin_hopper(self):
        self.result = basinhopping(
            func=self.obj_func,
            x0=[1500, 1000, 300],
            minimizer_kwargs={'args': (self.source_list, self.load_cases), 'method': 'SLSQP'}
        )
