import copy

import treelib

from core.source import Source
from core.sink import ElectricalSink
from core.transmission import Cable, Panel
from core.component import Component
from helpers.tree_utils import get_tree_edges, link_into_edge, get_largest_index
from helpers.input_utils import group_dictlist_by_key, import_csv_as_dictlist


class Model:

    def __init__(self):
        self._source_index = 0
        self._sink_index = 1
        self._source_list = []
        self._sink_tree = treelib.Tree()
        self._sink_tree.create_node("Root", 0, None, Root([0, 0, 0]))
        main_swbd = Panel([0, 0, 0], 1)
        main_swbd.name = "Main Switchboard"
        self._sink_tree.create_node(main_swbd.name, 1, 0, main_swbd)
        self.load_case_num = 0

    def solve(self, load_cases):
        root_powers = list()
        for load_case in load_cases:
            root_powers.append(self.solve_case(load_cases.index(load_case)))
        return root_powers

    def solve_case(self, load_case_num):
        self.load_case_num = load_case_num
        self.reset_components()

        # get root component and update its children
        root_comp = self._sink_tree.get_node(self._sink_tree.root).data
        root_comp.name = "Root"
        children_indices = self._sink_tree.is_branch(root_comp.get_index())
        children = [self._sink_tree.get_node(index).data for index in children_indices]
        root_comp.set_children(children)

        # solve root -> solve tree
        root_power = root_comp.get_power_in(self.load_case_num)
        return root_power

    def build(self):
        """
        Builds one line diagram from EPLA. This EPLA is hardcoded to the location ../data/EPLA_input.csv for now.
        """
        epla = import_csv_as_dictlist("../data/EPLA_input.csv")
        self.initialize_dictlist_to_tree(epla)
        self.add_cables()
        self.update_dependencies()

    def build_from_components_list(self, components):
        """
        Builds tree, chaining together components sequentially from list. This method is for testing behavior.
        :param components: list of Transmission Components with Sink as last element
        """
        # populate tree with Root -> Main SWBD -> all components
        for comp in components:
            self.add_sink_from_index(comp, self._sink_index)
        self.add_cables()
        self.update_dependencies()

    def initialize_dictlist_to_tree(self, components):
        """
        Builds tree, grouping components from EPLA dictlist into SWBS branches with one distribution panel each.
        :param components: dictlist of loads from epla
        :return: initialized tree appropriately sorted into groups
        """
        groups = group_dictlist_by_key(components, "SWBS")

        load_center_count = 1
        comp_id = 2
        for group in groups.values():
            panel = Panel([0, 0, 0])
            panel.name = "Load Center " + str(load_center_count)
            self._sink_tree.create_node(panel.name, comp_id, 1, panel)
            load_center_id = comp_id
            comp_id += 1
            load_center_count += 1

            for comp in group:
                location = [float(comp["Longitudinal Location"]),
                            float(comp["Transverse Location"]),
                            float(comp["Vertical Location"])]

                load_factors = list()
                load_factor_index = 1
                while ("Load Case " + str(load_factor_index)) in comp.keys():
                    load_factors.append(float(comp["Load Case " + str(load_factor_index)]))
                    load_factor_index += 1

                sink = ElectricalSink(location,
                                      float(comp["Power"]),
                                      load_factors,
                                      float(comp["Voltage"]),
                                      float(comp["Power Factor"]))
                sink.name = comp["Name"]
                self._sink_tree.create_node(sink.name, comp_id, load_center_id, sink)
                comp_id += 1

        self.reset_components()

    def add_cables(self):
        # add cables in between all component "edges" (sets of two linked components)
        cable_index = get_largest_index(self._sink_tree) + 1
        edges = get_tree_edges(self._sink_tree)
        for edge in edges:
            new_node = treelib.Node("Cable " + str(cable_index),
                                    cable_index,
                                    data=Cable([0, 0, 0]))
            new_node.data.name = "Cable " + str(cable_index)
            cable_index += 1
            self._sink_tree = link_into_edge(new_node, edge, self._sink_tree)
        self.reset_components()

    def update_dependencies(self):
        # TODO: remove this
        # this is a hasty fix for a more specific problem that every time we update the tree we need
        # to update each component

        # assign parents/children to components
        # this assigns a reference for each parent and child to each component
        # allowing us to recurse through all the children from the root

        # this may be a slow technique: would be preferable to avoid updating all components every time we run
        for node in self._sink_tree.all_nodes():
            children_indices = self._sink_tree.is_branch(node.identifier)
            children = [self._sink_tree.get_node(index).data for index in children_indices]
            node.data.set_children(children)
            if isinstance(node.data, Root):
                node.data.set_parents(None)
            else:
                parent = self._sink_tree.parent(node.identifier).data
                node.data.set_parents(parent)

    def reset_components(self):
        components = [node.data for node in self._sink_tree.all_nodes()]
        for comp in components:
            comp.reset()
        self.update_dependencies()

    def add_sink(self, new_sink, parent):
        self._sink_index += 1  # index starts at 1
        parent_index = parent.get_index()
        self._sink_tree.create_node(new_sink.name, self._sink_index, parent=parent_index, data=new_sink)
        new_sink.set_index(self._sink_index)
        self.update_dependencies()

    def add_sink_from_index(self, new_sink, parent_index):
        self._sink_index += 1  # index starts at 1
        self._sink_tree.create_node(new_sink.name, self._sink_index, parent=parent_index, data=new_sink)
        new_sink.set_index(self._sink_index)
        self.update_dependencies()

    def add_source(self, new_source):
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

    def print_tree(self):
        self._sink_tree.show()

    def export_old(self, filepath):
        pass

    def copy(self):
        return copy.copy(self)


class Root(Component):

    def __init__(self, location):
        super().__init__(location)
        self.name = "Root"

    def get_power_in(self, load_case_num):
        return self.get_power_out(load_case_num)
