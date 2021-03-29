import numpy as np
from scipy.optimize import minimize

from core.source import DieselShaftGenerator


def obj_func(engine_loading, source_list):
    fuel_burn = 0
    for index, engine in enumerate(source_list):
        # calculate the fuel burn of each engine and add it to the sum
        # TODO I don't think this working, engine loading is not be properly applied
        mechanical_load_wanted = engine_loading[2*index]
        electrical_load_wanted = engine_loading[2*index + 1]
        engine.set_power_level(mechanical_load_wanted, electrical_load_wanted)
        # remember to multiply by the index by 2 when getting engine loading
        # need to sum mechanical and electrical power before calling method
        fuel_burn += engine.fuel_consumption
        # solve emissions, .set_power_level calls .solve_emissions
        # get engine.fuel_consumption

    return fuel_burn


class EngineLoadSelector():
    def __init__(self, source_list, mechanical_power, electrical_power):
        self.source_list = source_list
        self.mechanical_power = mechanical_power
        self.electrical_power = electrical_power
        self.bounds = []
        self.constraints = []
        self.result = None

        self.set_power_levels()

    def set_power_levels(self):
        self.set_constraints()
        self.optimizer()

    def engine_loading(self):
        return self.result.x

    def set_constraints(self):
        # Set constraints so the required mechanical power and electrical power are generated
        def mechanical_constraint(engine_loading):
            return self.mechanical_power - np.sum(engine_loading[::2])

        def electrical_constraint(engine_loading):
            return self.electrical_power - np.sum(engine_loading[1::2])

        self.constraints.append({
            'type' : 'eq',
            'fun' : mechanical_constraint
        })

        self.constraints.append({
            'type': 'eq',
            'fun': electrical_constraint
        })

        for index, engine in enumerate(self.source_list):
            self.constraints = engine.constraint(self.constraints, index)

    def set_bounds(self):
        # Sets bounds so no engine is overloaded
        for engine in self.source_list:
            self.bounds = engine.bound(self.bounds)

    def optimizer(self):
        # There are two values in the list for each engine, first is the provided mechanical power and the second is the provided electrical power
        # noinspection PyTypeChecker
        self.result = minimize(
            fun=obj_func,
            args=self.source_list,
            x0 = [0] * 2 * len(self.source_list), #array of zeros twice the length of the source list
            constraints=self.constraints,
            method='SLSQP',
            options={'maxiter': 100, 'ftol': 1e0}
        )

