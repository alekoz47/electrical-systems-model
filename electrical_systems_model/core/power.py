

class Power:
    def __init__(self, power):
        self.power = power


class ElectricPower(Power):
    def __init__(self, power, voltage):
        super().__init__(power)
        self.voltage = voltage


class AlternatingCurrent(ElectricPower):
    def __init__(self, power, voltage, frequency, power_factor):
        super().__init__(power, voltage)
        self.frequency = frequency
        self.power_factor = power_factor


class SinglePhase(AlternatingCurrent):
    def __init__(self, power, voltage, frequency, power_factor):
        super().__init__(power, voltage,frequency,power_factor)
        self.current = self.power_factor * self.power / self.voltage


class ThreePhase(AlternatingCurrent):
    def __init__(self, power, voltage, frequency, power_factor):
        super().__init__(power, voltage, frequency, power_factor)
        self.current = numpy.sqrt(3) * self.power_factor * self.power / self.voltage


class DirectCurrent(ElectricPower):
    def __init__(self):
        super().__init__(power, voltage)
        self.current = self.power / self.voltage


class MechanicalPower(Power):
    def __init(self):
        super().__init__(power, rpm)
        self.rpm = rpm