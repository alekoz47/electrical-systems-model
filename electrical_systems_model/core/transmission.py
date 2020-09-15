from core.component import Component
from core.power import ThreePhase


class Transmission(Component):
    def __init__(self, location):
        super().__init__(location)

    def get_power_in(self):
        self.power_out = self.get_power_out()
        self.power_in = self.power_out
        return self.power_in


class Transformer(Transmission):

    def __init__(self, location, voltage_in, efficiency=0.97):
        super().__init__(location)
        self.voltage_in = voltage_in
        self.voltage_out = 0  # so we can track voltage_out in get_power_in
        self.efficiency = efficiency

    def get_power_in(self):
        super().get_power_in()
        self.voltage_out = self.power_out.voltage
        self.power_in = ThreePhase(self.power_out.power / self.efficiency,
                                   self.voltage_in,
                                   self.power_out.frequency,
                                   self.power_out.power_factor)
        return self.power_in


class Switchboard(Transmission):
    def __init__(self, location, efficiency=0.97):
        super().__init__(location)
        self.efficiency = efficiency

    def get_power_in(self):
        voltage_level_in = 0
        self.power_out = ThreePhase(1, 2, 3, 4)  # for testing only
        self.power_in = ThreePhase(self.power_out.power / self.efficiency,
                                   voltage_level_in,
                                   self.power_out.frequency,
                                   self.power_out.power_factor)


class Cable(Transmission):
    pass
