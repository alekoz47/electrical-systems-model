import copy

import treelib

from core.source import Source
from core.sink import ElectricalSink
from core.transmission import Cable, Panel
from core.component import Component
from helpers.tree_utils import get_tree_edges, link_into_edge, get_largest_index, list_of_type
from helpers.input_utils import group_dictlist_by_key, import_csv_as_dictlist
from helpers.math_utils import taxicab_ship_distance


class Model:

    def __init__(self):
        self._source_index = 0
        self._sink_index = 1
        self._source_list = []
        self._sink_tree = treelib.Tree()
        self._sink_tree.create_node("Root", 0, None, Root([0, 0, 0]))
        main_swbd = Panel([1, 1, 1], 1)  # TODO: place switchboard in a real location
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

            # place panel 1m transverse and 1m longitudinal from first component at same vertical location
            first_component = group[0].copy()
            first_location = [float(first_component["Longitudinal Location"]) + 1,
                              float(first_component["Transverse Location"]) + 1,
                              float(first_component["Vertical Location"])]
            panel = Panel(first_location)
            panel.name = "Load Center " + str(load_center_count)
            panel.group = group
            self._sink_tree.create_node(panel.name, comp_id, 1, panel)
            load_center_id = comp_id
            comp_id += 1
            load_center_count += 1

            for comp in group:
                location = [float(comp["Longitudinal Location"]),
                            float(comp["Transverse Location"]),
                            float(comp["Vertical Location"])]

                load_factors = list()
                load_factors.append(1)  # add connected load case for cable sizing
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

        # run other operations to organize the tree
        self.split_by_distance(50)
        self.split_by_num_loads(12)  # 12 loads is 36 poles for 3-phase, which means a large panel!

        self.reset_components()

    def split_by_distance(self, max_distance):
        """
        Splits subtrees of panels into new panels based on distance between groups.
        :param max_distance: maximum distance between loads and panel
        """
        # There are two good methods here. The easiest will be to separate the ship into quadrants but will require
        # additional data. The harder will be to separate components into clusters based on K-Means Clustering.
        # The simple method is to place the panel next to the location of the first component, then enforce a strict
        # distance limit on its other components. If one component does not meet this criterion, we create a new panel.
        # This third method is not great but will do for the current scope.

        panels = list_of_type(self._sink_tree, Panel)
        new_panels = list()

        for panel in panels:
            load_center_count = 1
            # we want to check each child of every panel and sort it into a better-fitting new panel if
            # it does not fit within the maximum distance of its original parent panel
            for child in [self._sink_tree.get_node(nid) for nid in self._sink_tree.is_branch(panel.identifier)]:
                if taxicab_ship_distance(child.data.location, panel.data.location) < max_distance:
                    # keep association with current panel
                    pass
                else:
                    chosen_panel = None
                    # attach to panel of same hierarchy with better fit
                    if new_panels:
                        # attempt to choose existing panel
                        for new_panel in new_panels:
                            if taxicab_ship_distance(child.data.location, new_panel.data.location) < max_distance \
                                    and new_panel.data.group == panel.data.group:
                                chosen_panel = new_panel
                    else:
                        # create new panel and add to list of new_panels
                        # choose new panel
                        location = list(map(sum, zip(child.data.location, [1, 1, 0])))  # prevent zero-length cable
                        new_panel = Panel(location)
                        new_panel.name = panel.data.name + "-" + str(load_center_count)
                        new_panel.group = panel.data.group
                        parent = self._sink_tree.parent(panel.identifier)
                        identifier = get_largest_index(self._sink_tree) + 1
                        # TODO: use default identifiers to avoid confusion
                        new_panel_node = treelib.Node(tag=new_panel.name,
                                                      identifier=identifier,
                                                      data=new_panel)
                        self._sink_tree.add_node(node=new_panel_node, parent=parent)
                        new_panels.append(new_panel_node)
                        chosen_panel = new_panel_node
                    # attach the misfit component to the chosen panel
                    self._sink_tree.move_node(child.identifier, chosen_panel.identifier)
                    load_center_count += 1

        self.reset_components()  # does this need to be run?

    def split_by_num_loads(self, max_num_loads):
        """
        Splits subtrees of panels into new panels based on number of loads.
        :param max_num_loads: maximum number of loads per panel
        """
        panels = list_of_type(self._sink_tree, Panel)
        new_panels = list()

        for panel in panels:
            load_center_count = 1
            # we want to check each child of every panel and sort it into a better-fitting new panel if
            # it does not fit within the maximum distance of its original parent panel
            if len(self._sink_tree.is_branch(panel.identifier)) > max_num_loads:
                # split branch in half!
                children = [self._sink_tree.get_node(nid) for nid in self._sink_tree.is_branch(panel.identifier)]
                left_children = children[:len(children) // 2]

                # attach left_children to new panel
                location = list(map(sum, zip(left_children[0].data.location, [1, 1, 0])))  # prevent zero-length cable
                left_panel = Panel(location)
                left_panel.name = panel.data.name + "-" + str(load_center_count)
                left_panel.group = panel.data.group
                parent = self._sink_tree.parent(panel.identifier)
                identifier = get_largest_index(self._sink_tree) + 1
                # TODO: use default identifiers to avoid confusion
                left_panel_node = treelib.Node(tag=left_panel.name,
                                               identifier=identifier,
                                               data=left_panel)
                self._sink_tree.add_node(node=left_panel_node, parent=parent)
                new_panels.append(left_panel_node)
                chosen_panel = left_panel_node
                for child in left_children:
                    self._sink_tree.move_node(child.identifier, chosen_panel.identifier)
                load_center_count += 1

        self.reset_components()  # does this need to be run?

    def split_by_current(self, max_current):
        pass

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

    def export_components(self):
        """
        Exports all components in tree to list of components by copying.
        :return: list of Component
        """
        component_references = self._sink_tree.all_nodes()
        component_copies = list()
        for comp in component_references:
            if isinstance(comp.data, Component) and not isinstance(comp.data, Root):
                component_copies.append(comp.data.copy())
        return component_copies

    def print_tree(self):
        self._sink_tree.show()

    def export_tree(self, show_cables=True):
        if show_cables:
            self._sink_tree.to_graphviz(filename="../data/graph1.gv", shape=u'circle', graph=u'digraph')
        else:
            tree = self.copy_tree()
            cables = list_of_type(tree, Cable)
            print(cables)
            for cable in cables:
                tree.link_past_node(cable.identifier)
            tree.to_graphviz(filename="../data/graph2.gv", shape=u'circle', graph=u'digraph')

    def export_old(self, filepath):
        pass

    def copy(self):
        return copy.copy(self)

    def copy_tree(self):
        return copy.copy(self._sink_tree)


class Root(Component):

    def __init__(self, location):
        super().__init__(location)
        self.name = "Root"

    def get_power_in(self, load_case_num):
        return self.get_power_out(load_case_num)
