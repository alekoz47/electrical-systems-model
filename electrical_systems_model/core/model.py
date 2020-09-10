import treelib as tree
from core.sink import Sink, MechanicalSink, ElectricalSink
from core.source import Source, Generator
from core.transmission import Transmission, Cable, Switchboard


class Model:

    def __init__(self):
        self._source_index = 0
        self._sink_index = 0
        self._source_tree = tree.Tree()
        self._source_tree.create_node("root", self._source_index)
        self._sink_tree = tree.Tree()
        self._sink_tree.create_node("root", self._sink_index)

    def solve(self):
        # root (empty) node is index 0
        # need to match roots of source and sink trees before evaluating
        starting_source = self._source_tree.leaves

        starting_sink = self._sink_tree.leaves

    def import_data(self, filepath):
        # TODO: add read-in from CSV file
        # this is an initial test of
        #   Generator -> Line -> Switchboard -> Line -> Motor

        # create components
        generator = Generator([0, 0, 0], 1)
        line1 = Cable()
        swbd = Switchboard()
        line2 = Cable()
        motor = ElectricalSink([0, 0, 0], 1, 120, 3)
        components = [generator, line1, swbd, line2, motor]

        # populate trees
        # right now, just connects components in order in a straight line
        # TODO: replace this loop with logic
        for comp in components:
            if isinstance(comp, Source):
                self.add_source(comp, self._source_index)
            else:
                self.add_sink(comp, self._sink_index)

        # assign parents/children to components
        for comp in components:
            if isinstance(comp, Source):
                comp.set_children(self._source_tree.is_branch(comp.get_index()))
                comp.set_parents(self._source_tree.parent)
            else:
                comp.set_children(self._sink_tree.is_branch(comp.get_index()))
                comp.set_parents(self._sink_tree.parent)

    def add_sink(self, new_sink, parent):
        self._sink_tree.create_node(new_sink._name(), self._sink_index, parent=parent, data=new_sink)
        self._sink_index += 1  # index starts at 1
        new_sink.set_index(self._sink_index)

    def add_source(self, new_source, parent):
        self._source_tree.create_node(new_source._name(), self._source_index, parent=parent, data=new_source)
        self._source_index += 1
        new_source.set_index(self._source_index)

    def remove_sink(self, sink):
        if sink.get_index() == 0:
            print("Error: Sink does not exist in tree. No sink removed.")
        self._sink_tree.link_past_node(sink.get_index())

    def remove_source(self, source):
        if source.get_index() == 0:
            print("Error: Source does not exist in tree. No source removed.")
        self._source_tree.link_past_node(source.get_index())
