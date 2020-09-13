from core.component import Component
from core.power import AlternatingCurrent


class Transmission(Component):
    def __init__(self, location):
        super().__init__(location)

    def get_power_in(self):
        pass


class Transformer(Transmission):
    def __init__(self, location, efficiency=0.97):
        super().__init__(location)
        self.efficiency = efficiency

    def get_power_in(self):
        self.power_out = AlternatingCurrent(1, 2, 3, 4)  # for testing purposes
        voltage_level_in = 0  # for testing purposes

        self.power_in = AlternatingCurrent(self.power_out.power / self.efficiency,
                                           voltage_level_in,
                                           self.power_out.frequency,
                                           self.power_out.power_factor)


class Switchboard(Transmission):
    def __init__(self, location, efficiency=0.97):
        super().__init__(location)
        self.efficiency = efficiency

    def get_power_in(self):
        voltage_level_in = 0
        self.power_out = AlternatingCurrent(1, 2, 3, 4)  # for testing only
        self.power_in = AlternatingCurrent(self.power_out.power / self.efficiency,
                                           voltage_level_in,
                                           self.power_out.frequency,
                                           self.power_out.power_factor)


class Cable(Transmission):
    pass
