import numpy
from abc import abstractmethod


class Power:
    def __init__(self, power):
        self.power = power

    @abstractmethod
    def add(self, power):
        pass

    def efficiency_loss(self, efficiency):
        self.power = self.power / efficiency


class ElectricPower(Power):
    def __init__(self, power, voltage):
        super().__init__(power)
        self.voltage = voltage
        self.current = None

    def add(self, power):
        self.power = self.power + power.power

    def resistance_loss(self, resistance):
        power_loss = self.current**2 * resistance
        self.power = self.power + power_loss



class AlternatingCurrent(ElectricPower):
    def __init__(self, power, voltage, frequency, power_factor=1):
        super().__init__(power, voltage)
        self.power = complex(power, 0)
        self.frequency = frequency
        self.power_factor = power_factor

    def add(self, power):
        super().add(power)
        self.power_factor = self.power.real / abs(self.power)


class SinglePhase(AlternatingCurrent):
    def __init__(self, power, voltage, frequency, power_factor):
        super().__init__(power, voltage, frequency, power_factor)
        self.current = self.power_factor * self.power / self.voltage

    def add(self, power):
        super().add(power)
        self.current = self.power_factor * self.power / self.voltage


class ThreePhase(AlternatingCurrent):
    def __init__(self, power, voltage, frequency, power_factor=1):
        super().__init__(power, voltage, frequency, power_factor)
        self.current = numpy.sqrt(3) * self.power_factor * self.power / self.voltage

    def add(self, power):
        super().add(power)
        self.current = numpy.sqrt(3) * self.power_factor * self.power / self.voltage


class DirectCurrent(ElectricPower):
    def __init__(self, power, voltage):
        super().__init__(power, voltage)
        self.current = self.power / self.voltage


class MechanicalPower(Power):
    def __init(self, power, rpm):
        super().__init__(power)
        self.rpm = rpm

    def add(self, power):
        pass
