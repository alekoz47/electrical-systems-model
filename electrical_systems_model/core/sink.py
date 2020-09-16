from core.component import Component
from core.power import ThreePhase, SinglePhase


class Sink(Component):
    def __init__(self, location, power):
        super().__init__(location)
        self.power_in = None

    def get_power_in(self):
        pass


class MechanicalSink(Sink):
    def __init__(self, location, power):
        super().__init__(location, power)


class ElectricalSink(Sink):
    def __init__(self, location, power_in, voltage, power_factor=1, frequency=60, phase=3):
        super().__init__(location, power_in)
        self.power_factor = power_factor
        self.frequency = frequency
        self.voltage = voltage
        self.phase = phase

    def get_power_in(self):
        if self.phase == 0:
            pass
        elif self.phase == 1:
            self.power_in = SinglePhase(self.power_in, self.voltage, self.frequency, self.power_factor)
        elif self.phase == 3:
            self.power_in = ThreePhase(self.power_in, self.voltage, self.frequency, self.power_factor)
        else:
            print("Please enter a valid phase (DC: 0, Single: 1, Triple: 3)")
