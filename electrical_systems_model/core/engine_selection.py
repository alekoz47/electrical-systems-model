from core.engine_rating import EngineRatingSelector
from core.source import DieselMechanical, DieselGenerator, DieselShaftGenerator
from helpers.optimization_utils import pareto_optimize


class EngineSelector:
    def __init__(self, load_cases):
        self.load_cases = load_cases

        # choose maximum mechanical and maximum electrical power as design cases
        self.mechanical_power = max([case["Mechanical Power"] for case in load_cases])
        self.electrical_power = max([case["Electrical Power"] for case in load_cases])
        self.total_power = self.mechanical_power + self.electrical_power

        # generate engine permutations for class
        self.engines = list()
        self.generate_engines(self.generate_permutations())

        # need to pass list of engine objects + list of load cases to engine_rating
        # generate dictionary of engine selection, rating, loading at each load case, and vector of objectives
        self.results = None

    def run_optimization(self):
        raw_results = list()
        for engine_set in self.engines:
            rating_selector = EngineRatingSelector(engine_set, self.load_cases)
            fuel_consumption = rating_selector.result["fun"]  # weighted average fuel consumption
            emissions = sum(zip([engine.get_emissions() for engine in engine_set]))  # FIXME: change to weighted average
            raw_results.append({"Engine Set": engine_set,
                                "Objective": [fuel_consumption, emissions]
                                })

        self.results = pareto_optimize(raw_results)

    def generate_permutations(self):
        is_all_mechanical = self.electrical_power == 0
        is_all_electrical = self.mechanical_power == 0

        configurations = list()
        for i in range(5):
            for j in range(5):
                for k in range(5):
                    configurations.append([i, j, k])

        valid_configurations = list()
        for config in configurations:
            if is_valid_configuration(config, is_all_mechanical, is_all_electrical):
                valid_configurations.append(config)
        return valid_configurations

    def generate_engines(self, permutations):
        for config in permutations:
            engine_set = list()
            if config[0] != 0:
                engine_set.append([DieselMechanical([0, 0, 0], self.mechanical_power / config[0] * 1.1)] * config[0])
            if config[1] != 0:
                engine_set.append([DieselGenerator([0, 0, 0], self.electrical_power / config[1] * 1.1)] * config[1])
            if config[2] != 0:
                engine_set.append([DieselShaftGenerator([0, 0, 0], self.total_power / config[2] * 1.1)] * config[2])
            self.engines.append(engine_set)
        for engine_set in self.engines:
            if engine_set == list():  # purge empties
                self.engines.remove(engine_set)


def is_valid_configuration(config, is_all_mechanical, is_all_electrical):
    return not (config[0] == 3 or
                config[2] == 3 or
                sum(config) == 0 or
                sum(config) > 8 or
                (config[0] > 0 and config[2] > 0) or
                ((not (is_all_mechanical or is_all_electrical)) and
                 (config[1] == 1 and config[2] == 0)) or
                ((is_all_electrical or
                  not (is_all_mechanical or is_all_electrical)) and
                 (config[0] == 0 and config[2] == 0)))
