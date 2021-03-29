import copy
from abc import ABC, abstractmethod

import numpy


class PowerInterface(ABC):
    @abstractmethod
    def add(self, power):
        pass

    @abstractmethod
    def apply_efficiency_loss(self, efficiency):
        pass

    def copy(self):
        return copy.copy(self)


class SinglePhaseElectricalPower(PowerInterface):
    # TODO: refactor to include phase switch to eliminate repeating ourselves
    # this would include phase (int) in arguments for creation
    # and would require additional handling in __init__, add, and resistance_loss methods
    def __init__(self, power, voltage, frequency, power_factor):
        self.voltage = voltage
        self.frequency = frequency
        self.power_factor = power_factor
        phase_quadrant = power_factor / abs(power_factor)
        real_power = power * power_factor / phase_quadrant
        imag_power = numpy.sqrt(power**2 - real_power**2) * phase_quadrant
        self.power = complex(real_power, imag_power)
        self.current = abs(self.power) / self.voltage

    def add(self, power):
        self.power = self.power + power.power
        self.power_factor = self.power.real / abs(self.power)
        self.current = abs(self.power) / (numpy.sqrt(3) * self.voltage)

    def apply_efficiency_loss(self, efficiency):
        self.power = self.power / efficiency

    def apply_resistance_loss(self, resistance):
        self.current = abs(self.power) / (numpy.sqrt(3) * self.voltage)
        current_phase = self.current
        loss_phase = current_phase**2 * resistance
        power_loss = loss_phase
        self.power = self.power + power_loss


class ThreePhaseElectricalPower(PowerInterface):
    # TODO: refactor to include phase switch to eliminate repeating ourselves
    # this would include phase (int) in arguments for creation
    # and would require additional handling in __init__, add, and resistance_loss methods
    def __init__(self, power, voltage, frequency, power_factor):
        self.voltage = voltage
        self.frequency = frequency
        self.power_factor = power_factor
        phase_quadrant = power_factor / abs(power_factor)
        real_power = power * power_factor / phase_quadrant
        imag_power = numpy.sqrt(power**2 - real_power**2) * phase_quadrant
        self.power = complex(real_power, imag_power)
        self.current = abs(self.power) / (numpy.sqrt(3) * self.voltage)

    def add(self, power):
        self.power = self.power + power.power
        self.power_factor = self.power.real / abs(self.power)
        self.current = abs(self.power) / (numpy.sqrt(3) * self.voltage)

    def apply_efficiency_loss(self, efficiency):
        self.power = self.power / efficiency

    def apply_resistance_loss(self, resistance):
        self.current = abs(self.power) / (numpy.sqrt(3) * self.voltage)
        current_phase = self.current / numpy.sqrt(3)
        loss_phase = current_phase**2 * resistance
        power_loss = 3 * loss_phase
        self.power = self.power + power_loss


class DirectElectricalPower(PowerInterface):
    # TODO: implement this class
    def __init__(self, power, voltage):
        self.power = power
        self.voltage = voltage
        self.current = self.power / self.voltage

    def add(self, power):
        pass

    def apply_efficiency_loss(self, efficiency):
        self.power = self.power / efficiency


class MechanicalPower(PowerInterface):
    # TODO: implement this class
    def __init__(self, power, rpm):
        self.power = power
        self.rpm = rpm

    def add(self, power):
        pass

    def apply_efficiency_loss(self, efficiency):
        self.power = self.power / efficiency
