import sys
import os

from unittest import TestCase

from context import Cable

sys.path.insert(0, os.path.abspath("../electrical_systems_model/core"))

class MockComponent:
    def __init__(self, location, power_out):
        self.location = location
        self.power_out = power_out

class TestCable(TestCase):
    data_path =

    def test_distance_finder(self):
        mock_child = MockComponent([0,0,0], None)
        mock_parent = MockComponent([1,1,1], None)
        test_cable = Cable([0, 0, 0])
        test_cable.set_parents(mock_parent)
        test_cable.set_children(mock_child)
        test_cable.set_distance()

        expected_distance = 3
        self.assertAlmostEqual(self.test_cable.length, expected_distance)



    def test_get_power_in(self):
        PARENT = Transformer([100, 12, 20], 440)
        CHILD = ElectricalSink([125, 3, 5], 10000, 220)
        CABLE = Cable([0, 0, 0])
        CABLE.set_parents(PARENT)
        CABLE.set_children([CHILD])
        CABLE.get_power_in()
        # Fix later



        self.fail()


class TestTransformer(TestCase):
    def test_get_power_in(self):
        self.fail()
