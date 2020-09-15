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

    def get_parents(self):
        return self._parents

    def get_children(self):
        return self._children

    def get_index(self):
        return self._index

    @abstractmethod
    def get_power_in(self):
        pass

    def get_power_out(self):
        for child in self._children:
            self.power_out.add(child.get_power_in())
        return self.power_out

    def set_parents(self, parents):
        self._parents = parents

    def set_children(self, children):
        self._children = children

    def set_index(self, index):
        self._index = index
