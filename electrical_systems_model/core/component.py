from core.power import Power


class Component:

    def __init__(self, parents=None, children=None):
        self._parents = parents
        self._children = children

    def get_parents(self):
        return self._parents

    def get_children(self):
        return self._children

    def add_parents(self, new_parents):
        self._parents.add(new_parents)

    def add_children(self, new_children):
        self._children.add(new_children)
