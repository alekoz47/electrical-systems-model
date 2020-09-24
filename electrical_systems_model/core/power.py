import copy

import numpy


class Power:
    def __init__(self, power):
        self.power = power

    def add(self, power):
        # TODO: figure out how to add powers of different voltages / frequencies
        # currently we're just going to cast with matching voltage and power
        # this may break Transformer behavior
        # self = type(power).cast(self)
        pass

    def efficiency_loss(self, efficiency):
        self.power = self.power / efficiency

    def copy(self):
        return copy.copy(self)

    # @classmethod
    # def cast(cls, power_object):
    #     power_object.__class__ = cls
    #     return power_object


class ElectricPower(Power):
    def __init__(self, power, voltage):
        super().__init__(power)
        self.voltage = voltage
        self.current = None

    def add(self, power):
        super().add(power)
        self.power = self.power + power.power

    def resistance_loss(self, resistance):
        power_loss = self.current**2 * resistance
        self.power = self.power + power_loss


class AlternatingCurrent(ElectricPower):
    def __init__(self, power, voltage, frequency, power_factor=1):
        super().__init__(power, voltage)
        real_power = power * power_factor
        imag_power = numpy.sqrt(power**2 - real_power**2)
        self.power = complex(real_power, imag_power)
        self.frequency = frequency
        self.power_factor = power_factor

    def add(self, power):
        super().add(power)
        self.power_factor = self.power.real / abs(self.power)


class SinglePhase(AlternatingCurrent):
    def __init__(self, power, voltage, frequency, power_factor):
        super().__init__(power, voltage, frequency, power_factor)
        self.current = abs(self.power) / self.voltage

    def add(self, power):
        super().add(power)
        self.current = abs(self.power) / self.voltage


class ThreePhase(AlternatingCurrent):
    def __init__(self, power, voltage, frequency, power_factor):
        super().__init__(power, voltage, frequency, power_factor)
        self.current = numpy.sqrt(3) * abs(self.power) / self.voltage

    def add(self, power):
        super().add(power)
        self.current = numpy.sqrt(3) * abs(self.power) / self.voltage


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
