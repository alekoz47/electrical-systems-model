import numpy as np
from scipy.optimize import minimize
from core.engine_loading import EngineLoadSelector


# This is a test that should be moved somewhere else
test_load_case = {
    'Name' : 'Test Load Case',
    'Mechanical Power' : 0,
    'Electrical Power' : 500,
    'Use Factor' : 1
}

old_engine_loading = []

def obj_func(engine_rating, source_list, load_cases):
    normalized_fuel_burn = 0
    new_engine_loading = []
    global old_engine_loading

    for index, source in enumerate(source_list):
        source.power_brake = engine_rating[index]

    # for loop for each operating case
    for index, case in enumerate(load_cases):
        mechanical_power = case['Mechanical Power']
        electrical_power = case['Electrical Power']
        case_percent = case['Use Factor']

        # Make initial guess of loading the previous iterations optimized loadings

        load_case_optimizer = EngineLoadSelector(source_list, mechanical_power, electrical_power, old_engine_loading[index])
        case_fuel_burn = load_case_optimizer.result.fun
        normalized_fuel_burn += case_percent * case_fuel_burn

        new_engine_loading.append(load_case_optimizer.result.x)

    print('Engine Ratings:', engine_rating)
    print('Engine Loading:', new_engine_loading)
    print('Normalized Fuel Burn (MT/hr):', normalized_fuel_burn)
    print()

    old_engine_loading = new_engine_loading

    return normalized_fuel_burn

class EngineRatingSelector():
    def __init__(self, source_list, load_cases):
        global old_engine_loading
        old_engine_loading = [[0] * 2 * len(source_list)] * len(load_cases)
        print(old_engine_loading)
        self.source_list = source_list
        self.load_cases = load_cases
        self.bounds = []
        self.constraints = []
        self.result = None
        self.engine_loading = []
        self.optimize_engine_ratings()


        print(old_engine_loading)

    def optimize_engine_ratings(self):
        # self.set_constraints()
        self.optimizer()

    def set_constraints(self):

        # TODO Set constraint that engine rating need to be 110% of maximum electrical and maximum mechanical power
        # TODO ineq constraint
        # Someting different for shaft power

        for index, source in enumerate(self.source_list):
            def non_zero_constraint(engine_loading):

                return self.power_brake - self.power

            self.constraints.append({
                'type': 'ineq',
                'fun': non_zero_constraint
            })


    def optimizer(self):
        self.result = minimize(
            fun=obj_func,
            args=(self.source_list, self.load_cases),
            #x0=[1500]*len(self.source_list),
            x0=[1500, 1000, 500],
            bounds=[(0, 5000)]*len(self.source_list),
            #constraints = self.constraints,
            method = 'SLSQP',
            options = {'maxiter': 100, 'ftol': 1e-12}
        )

