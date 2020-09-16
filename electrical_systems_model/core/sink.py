from core.component import Component
from core.power import Power


class Sink(Component):
    def __init__(self, location, power):
        super().__init__(location)
        self.power_in = power

    def get_power_in(self):
        return self.power_in


class MechanicalSink(Sink):
    def __init__(self, location, power):
        super().__init__(location, power)


class ElectricalSink(Sink):
    def __init__(self, location, power_in, voltage, phase=3):
        super().__init__(location, power_in)
        self.voltage_level = voltage
        self.phase = phase
