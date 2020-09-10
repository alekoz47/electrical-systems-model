from core.component import Component
from core.power import Power


class Sinks:
    def __init__(self, parents, children, power, location):
        super(Sinks).__init__(parents, children)
        self.power_in = power
        self.location = location  # location is a 3d vector


class MechanicalSink(Sinks):
    def __init__(self, parents, children, power_in, location):
        super(MechanicalSink).__init__(parents, children, power_in, location)


class ElectricalSink(Sinks):
    def __init__(self, parents, children, power_in, location, voltage, phase):
        super(ElectricalSink).__init__(parents, children, power_in, location)
        self.voltage_level = voltage
        self.phase = phase


