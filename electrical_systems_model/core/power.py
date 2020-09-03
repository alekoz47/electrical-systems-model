import numpy

class Power:
    def __init__(self):
        self.power = None

class ElectricPower(Power):
    def __init__(self):
        self.voltage = None


class AlternatingCurrent(ElectricPower):
    def __init__(self):
        self.frequency = None
        self.phaseangle = None


class SinglePhase(AlternatingCurrent):
    def current(self):
        self.current = self.phaseangle * self.power / self.voltage
        return self.current

class ThreePhase(AlternatingCurrent):
    def current(self):
        self.current = numpy.sqrt(3) * self.power / self.voltage
        return self.current


class DirectCurrent(ElectricPower):
    def current(self):
        i = self.power/self.voltage
        return i

class MechanicalPower(Power):
    def __init(self):
        self.rpm = None


