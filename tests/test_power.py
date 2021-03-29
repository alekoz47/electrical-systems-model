from unittest import TestCase

from context import ThreePhaseElectricalPower


class TestThreePhase(TestCase):
    POWER = 10
    VOLTAGE = 120
    FREQUENCY = 60
    POWER_FACTOR = 0.8
    TEST_POWER = ThreePhaseElectricalPower(POWER, VOLTAGE, FREQUENCY, POWER_FACTOR)

    def test_add(self):
        # test addition with positive power factor
        power = ThreePhaseElectricalPower(self.POWER,
                                          self.VOLTAGE,
                                          self.FREQUENCY,
                                          self.POWER_FACTOR - 0.1)
        expected_power = ThreePhaseElectricalPower(19.9423454273191,
                                                   self.VOLTAGE,
                                                   self.FREQUENCY,
                                                   0.752168297087636)
        test_power = self.TEST_POWER.copy()
        test_power.add(power)

        self.assertAlmostEqual(test_power.power, expected_power.power)
        self.assertAlmostEqual(test_power.voltage, expected_power.voltage)
        self.assertAlmostEqual(test_power.frequency, expected_power.frequency)
        self.assertAlmostEqual(test_power.power_factor, expected_power.power_factor)
        self.assertAlmostEqual(test_power.current, expected_power.current)

        # test addition with negative power factor
        power = ThreePhaseElectricalPower(self.POWER,
                                          self.VOLTAGE,
                                          self.FREQUENCY,
                                          -1 * self.POWER_FACTOR)
        expected_power = ThreePhaseElectricalPower(16,
                                                   self.VOLTAGE,
                                                   self.FREQUENCY,
                                                   1)
        test_power = self.TEST_POWER.copy()
        test_power.add(power)

        self.assertAlmostEqual(test_power.power, expected_power.power)
        self.assertAlmostEqual(test_power.voltage, expected_power.voltage)
        self.assertAlmostEqual(test_power.frequency, expected_power.frequency)
        self.assertAlmostEqual(test_power.power_factor, expected_power.power_factor)
        self.assertAlmostEqual(test_power.current, expected_power.current)
