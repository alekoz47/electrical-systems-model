from core.power import Power
from abc import ABC, abstractmethod

class Component:

    _name = ""
    _index = 0

    def __init__(self, location, parents=None, children=None):
        self.location = location
        self._parents = parents
        self._children = children
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

    def set_parents(self, parents):
        self._parents = parents

    def set_children(self, children):
        self._children = children

    def set_index(self, index):
        self._index = index
