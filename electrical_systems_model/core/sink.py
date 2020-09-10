from core.component import Component
from core.power import Power


class Sinks(Component):
    def __init__(self, location, parents, children, power):
        super().__init__(location, parents, children)
        self.power_in = power



class MechanicalSink(Sinks):
    def __init__(self, location, parents, children, power):
        super().__init__(parents, children, power, location)


class ElectricalSink(Sinks):
    def __init__(self, location, parents, children, power_in, voltage, phase):
        super().__init__(location, parents, children, power_in)
        self.voltage_level = voltage
        self.phase = phase


