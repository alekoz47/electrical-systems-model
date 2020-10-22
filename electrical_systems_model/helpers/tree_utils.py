import treelib as tree


def get_tree_edges(tt):
    # returns list of edges given tree
    return _get_tree_edges_acc(tt, tt.root, list())


def _get_tree_edges_acc(tt, node, acc):
    # accumulator, not meant to be called
    # tied to get_tree_edges(tt)
    # TODO: convert to tail recursion with *args for branches
    if not tt.is_branch(node):
        return acc
    else:
        for child in tt.is_branch(node):
            acc.append([node, child])
            _get_tree_edges_acc(tt, child, acc)
    return acc


def link_into_edge(node, edge, tt):
    # place new node in tree between parent and child
    # 1: remove subtree of child node
    # 2: add new node to parent
    # 3: re-attach subtree to new node
    parent = edge[0]
    child = edge[1]
    subtree = tt.remove_subtree(child)
    tt.add_node(node, parent)
    tt.paste(node.identifier, subtree)

    # the above technique involves a lot of overhead
    # TODO: implement this more efficiently using the following method:
    # 1: add the node to the parent node (dangling)
    # 2: "snap" the node to the child node by correcting the parent reference of the child node

    return tt


def insert_node(node, target, tt):
    parent = tt.parent(target)
    children = tt.get_branch(target)
    subtrees = list()
    for child in children:
        subtrees.append(tt.remove(child))
    tt.add_node(node, parent)
    for subtree in subtrees:
        tt.paste(node.identifier, subtree)
    return tt


def get_largest_index(tt):
    largest_index = 0
    indices = [node.identifier for node in tt.all_nodes()]
    for index in indices:
        if largest_index < index:
            largest_index = index
    return largest_index


def convert_node_to_tag(node, tt):
    return tt.get_node(node).tag
