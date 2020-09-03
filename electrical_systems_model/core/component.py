import power


class Component:

    def __init__(self, parents=None, children=None):
        self._parents = parents
        self._children = children

    def get_parents(self):
        return self._parents

    def get_children(self):
        return self._children
