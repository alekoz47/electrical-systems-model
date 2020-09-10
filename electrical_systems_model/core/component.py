from core.power import Power
from abc import ABC, abstractmethod

class Component:

    _name = ""
    _index = 0

    def __init__(self, location):
        self.location = location
        self._parents = None
        self._children = None
        self.power_in = None
        self.power_out = None

    def get_parents(self):
        return self._parents

    def get_children(self):
        return self._children

    def get_index(self):
        return self._index

    @abstractmethod
    def get_power_in(self):
        pass

    def set_index(self, index):
        self._index = index
