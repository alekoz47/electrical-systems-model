import numpy
from core.component import Component
from core.power import ThreePhaseElectricalPower, SinglePhaseElectricalPower


class Sink(Component):

    def __init__(self, location, power, load_factors):
        super().__init__(location)
        self.load_factors = load_factors
        self.power_connected = power
        self.power_list = [self.power_connected * factor for factor in load_factors]
        self.power = None

    def get_power_in(self, load_case_num):
        super().get_power_in(load_case_num)
        self.power = self.power_list[load_case_num]
        pass


class MechanicalSink(Sink):
    def __init__(self, location, power, load_factors):
        super().__init__(location, power, load_factors)


class ElectricalSink(Sink):
    def __init__(self, location, power, load_factors, voltage, power_factor=1, frequency=60, phase=3):
        super().__init__(location, power, load_factors)
        self.power_factor = power_factor
        self.frequency = frequency
        self.voltage = voltage
        self.phase = phase

    def get_power_in(self, load_case_num):
        super().get_power_in(load_case_num)
        if self.phase == 0:
            pass
        elif self.phase == 1:
            self.power_in = SinglePhaseElectricalPower(self.power, self.voltage, self.frequency, self.power_factor)
        elif self.phase == 3:
            self.power_in = ThreePhaseElectricalPower(self.power, self.voltage, self.frequency, self.power_factor)
        else:
            print("Please enter a valid phase (DC: 0, Single: 1, Triple: 3)")
        return self.power_in
