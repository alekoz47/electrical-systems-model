from core.component import Component
from core.power import Power
import numpy


class Power:
    def __init__(self):
        self.power = None


class ElectricPower(Power):
    def __init__(self):
        super().__init__()
        self.voltage = None


class AlternatingCurrent(ElectricPower):
    def __init__(self):
        super().__init__()
        self.frequency = None
        self.power_factor = None


class SinglePhase(AlternatingCurrent):
    def __init__(self):
        super().__init__()

    def current(self):
        self.current = self.power_factor * self.power / self.voltage
        return self.current


class ThreePhase(AlternatingCurrent):
    def __init__(self):
        super().__init__()

    def current(self):
        self.current = numpy.sqrt(3) * self.power_factor * self.power / self.voltage
        return self.current


class DirectCurrent(ElectricPower):
    def __init__(self):
        super().__init__()

    def current(self):
        self.current = self.power / self.voltage
        return self.current


class MechanicalPower(Power):
    def __init(self):
        super().__init__()
        self.rpm = None
