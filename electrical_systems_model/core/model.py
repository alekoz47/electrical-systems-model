import treelib as tree
from core.sink import Sink, ElectricalSink
from core.source import Source
from core.transmission import Cable, Transformer
from core.component import Component


class Model:

    def __init__(self):
        self._source_index = 0
        self._sink_index = 0
        self._source_list = []
        self._sink_tree = tree.Tree()
        self._sink_tree.create_node("root", 0, None, Root([0, 0, 0]))

    def solve_model(self):
        # root (empty) node is index 0 for each tree
        # traverse sink tree from leaves to root, finding Power at root
        # link sink root to source root
        # TODO: decide on linking between sink and source roots
        # traverse source tree from root to leaves, finding Power at each source
        # TODO: implement smarter Power setting at sources
        root_power = self._sink_tree.get_node(self._sink_tree.root).get_power_in()
        return root_power

    # def _solve_tree(self, comp_tree):
    #     # traverses tree and
    #     node_id = 0
    #     power_out = 0
    #     power = self._solve_node(comp_tree, node_id, power_out)
    #     return comp_tree.get_node(0)
    #
    # def _solve_node(self, comp_tree, node_id, power_out):
    #     # solves the given node and returns its input power
    #     comp = comp_tree.get_node(node_id)
    #     if not isinstance(comp, Sink):
    #         comp.power_out = power_out
    #     return comp.get_power_in()

    def import_data(self, filepath):
        # TODO: add read-in from CSV file
        # this is an initial test of
        #   Root -> Line -> Switchboard -> Line -> Motor

        # create components
        line1 = Cable([0, 0, 0])
        transformer = Transformer([0, 0, 0], 440)
        line2 = Cable([0, 0, 0])
        motor = ElectricalSink([0, 0, 0], 10, 220)
        components = [line1, transformer, line2, motor]

        # populate trees
        # right now, just connects components in order in a straight line
        # TODO: replace this loop with logic for populating OLD
        for comp in components:
            if isinstance(comp, Source):
                self.add_source(comp, self._source_index)
            else:
                self.add_sink(comp, self._sink_index)

        # assign parents/children to components
        for comp in components:
            if isinstance(comp, Source):
                pass
            else:
                comp.set_children(self._sink_tree.is_branch(comp.get_index()))
                comp.set_parents(self._sink_tree.parent)

    def add_sink(self, new_sink, parent):
        self._sink_tree.create_node(new_sink.name, self._sink_index, parent=parent, data=new_sink)
        self._sink_index += 1  # index starts at 1
        new_sink.set_index(self._sink_index)

    def add_source(self, new_source, parent):
        self._source_list.append(new_source)
        self._source_index += 1

    def remove_sink(self, sink):
        if sink.get_index() == 0:
            print("Error: Sink does not exist in tree. No sink removed.")
        self._sink_tree.link_past_node(sink.get_index())

    def remove_source(self, source):
        # TODO: find more robust method for checking if index is valid
        # if source.get_index() == 0:
        #     print("Error: Source does not exist in list. No source removed.")
        self._source_list.pop(source.get_index())


class Root(Component):

    def __init__(self, location):
        super().__init__(location)

    def get_power_in(self):
        return self.get_power_out()
