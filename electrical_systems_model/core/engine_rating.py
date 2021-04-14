import numpy as np
from scipy.optimize import minimize
from core.engine_loading import EngineLoadSelector


# This
test_load_case = {
    'Name' : 'Test Load Case',
    'Mechanical Power' : 0,
    'Electrical Power' : 50,
    'Use Factor' : 1
}


def obj_func(engine_rating, source_list, load_cases):
    normalized_fuel_burn = 0

    for index, source in enumerate(source_list):
        source.power_brake = engine_rating[index]

    # for loop for each operating case
    for case in load_cases:
        mechanical_power = case['Mechanical Power']
        electrical_power = case['Electrical Power']
        case_percent = case['Use Factor']

        load_case_optimizer = EngineLoadSelector(source_list, mechanical_power, electrical_power)
        case_fuel_burn = load_case_optimizer.result.fun
        normalized_fuel_burn += case_percent * case_fuel_burn

    return normalized_fuel_burn

class EngineRatingSelector():
    def __init__(self, source_list, load_cases):
        self.source_list = source_list
        self.load_cases = load_cases
        self.bounds = []
        self.constraints = []
        self.result = None
        self.optimize_engine_ratings()

    def optimize_engine_ratings(self):
        # self.set_constraints()
        self.optimizer()

    def set_constraints(self):
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
            x0=[1]*len(self.source_list),
            bounds=[(0, 100)]*len(self.source_list),
            #constraints = self.constraints,
            method = 'SLSQP',
            options = {'maxiter': 100, 'ftol': 1e-12}
        )

