from core.power import Power


class Component:

    def __init__(self, parents=None, children=None):
        self._parents = parents
        self._children = children
        self.power_in = None
        self.power_out = None

    def get_parents(self):
        return self._parents

    def get_children(self):
        return self._children

    #@abstractmethod
    def get_power_in(self):
        pass
