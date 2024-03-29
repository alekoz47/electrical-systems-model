import copy
from abc import abstractmethod


class Component:

    def __init__(self, location):
        self.location = location
        self._parents = None
        self._children = None
        self._index = 0
        self.power_in = None
        self.power_out = None
        self.name = ""
        self.load_case_num = 0

    def get_parents(self):
        return self._parents

    def get_children(self):
        return self._children

    def get_index(self):
        return self._index

    @abstractmethod
    def get_power_in(self, load_case_num):
        self.load_case_num = load_case_num
        pass

    def get_power_out(self, load_case_num):
        # this assumes the children all share voltage and frequency
        # children of different voltages should be split by a transformer and panel
        # default_power acts as an accumulator
        default_power = self._children[0].get_power_in(load_case_num)
        default_power.power = 0
        for child in self._children:
            default_power.add(child.get_power_in(load_case_num))
        self.power_out = default_power
        return self.power_out

    def set_parents(self, parents):
        self._parents = parents

    def set_children(self, children):
        self._children = children

    def reset(self):
        self.power_in = None
        self.power_out = None
        self._children = None
        self._parents = None

    def set_index(self, index):
        self._index = index

    def copy(self):
        return copy.copy(self)
