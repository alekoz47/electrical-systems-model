from core.component import Component
from core.power import AlternatingCurrent


class Transmission(Component):
    def __init__(self, location, parents, children):
        super().__init__(parents, children)


class Transformer(Transmission):
    def __init__(self, location, parents, children, efficiency=0.97):
        super().__init__(location, parents, children)
        self.efficiency = efficiency

    def get_power_in(self):
        self.power_out = AlternatingCurrent(1,2,3,4)
        voltage_level_in = 0

        self.power_in = AlternatingCurrent(self.power_out.power / self.efficiency,
                                           voltage_level_in,
                                           self.power_out.frequency,
                                           self.power_out.power_factor)
