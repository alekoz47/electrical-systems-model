import treelib

from core.model import Root
from core.transmission import Panel, Transformer
from core.sink import ElectricalSink


def grouping_by_key(components, key):
    grouping = dict()
    for comp in components:
        if comp[key] in grouping:
            grouping[key] = list()
        grouping[key].append(comp[key])
    return grouping


def create_tree_from_components(components, system_data):
    groups = grouping_by_key(components, "Group")

    tree = treelib.Tree()
    tree.create_node("Root", 0, None)
    tree.create_node("Main Switchboard", 1, 0)

    load_center_count = 1
    comp_id = 2
    for group in groups:
        tree.create_node("Load Center" + str(load_center_count), comp_id, 1)
        load_center_id = comp_id
        comp_id += 1
        load_center_count += 1

        for comp in group:
            tree.create_node(comp["Name"], comp_id, load_center_id)
            comp_id += 1
    return tree
