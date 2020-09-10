#from core.component import Component
#from core.power import Power

import numpy as np

class Sinks:
    def __init__(self, power, location,):
        self.power_in = power
        self.location = location  # location is a 3d vector



class MechanicalSink(Sinks):
    def __init__(self, power, location):
        super().__init__(power, location)


class ElectricalSink(Sinks):
    def __init__(self, power, location, voltage, phase):
        super().__init__(power, location)
        self.voltage_level = voltage
        self.phase = phase


