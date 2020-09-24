from unittest import TestCase

from context import ThreePhase


class TestThreePhase(TestCase):
    POWER = 10
    VOLTAGE = 120
    FREQUENCY = 60
    POWER_FACTOR = 0.8

    test_power = ThreePhase(POWER, VOLTAGE, FREQUENCY, POWER_FACTOR)

    def test_add(self):
        power = ThreePhase(self.POWER, self.VOLTAGE, self.FREQUENCY, self.POWER_FACTOR - 0.1)
        expected_power = ThreePhase(19.9423454273191, self.VOLTAGE, self.FREQUENCY, 0.752168297087636)
        self.test_power.add(power)

        self.assertAlmostEqual(self.test_power.power, expected_power.power)
        self.assertAlmostEqual(self.test_power.voltage, expected_power.voltage)
        self.assertAlmostEqual(self.test_power.frequency, expected_power.frequency)
        self.assertAlmostEqual(self.test_power.power_factor, expected_power.power_factor)
        self.assertAlmostEqual(self.test_power.current, expected_power.current)
