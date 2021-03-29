import sys
import os

from unittest import TestCase

from context import Cable, Transformer, ElectricalSink

sys.path.insert(0, os.path.abspath("../electrical_systems_model/core"))


class MockComponent:
    def __init__(self, location, power_out):
        self.location = location
        self.power_out = power_out


class TestCable(TestCase):

    def test_distance_finder(self):
        mock_child = MockComponent([0, 0, 0], None)
        mock_parent = MockComponent([1, 1, 1], None)
        test_cable = Cable([0, 0, 0])
        test_cable.set_parents(mock_parent)
        test_cable.set_children(mock_child)
        test_cable.set_distance()

        expected_distance = 3
        self.assertAlmostEqual(test_cable.length, expected_distance)

    def test_get_power_in(self):
        parent = Transformer([100, 12, 20], 440)
        child = ElectricalSink([125, 3, 5], 10000, [1], 220)
        cable = Cable([0, 0, 0])
        cable.set_parents(parent)
        cable.set_children([child])
        cable.get_power_in(0)
        # Fix later

        self.fail()


class TestTransformer(TestCase):
    def test_get_power_in(self):
        self.fail()
