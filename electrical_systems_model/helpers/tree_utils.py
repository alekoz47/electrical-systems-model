import treelib as tree


def get_tree_edges(tt):
    # returns list of edges given tree
    return _get_tree_edges_acc(tt, tt.root, list())


def _get_tree_edges_acc(tt, node, acc):
    # accumulator, not meant to be called
    # tied to get_tree_edges(tt)
    if tt.is_branch(node) is list():
        return acc
    else:
        for child in tt.is_branch(node):
            acc.append([node, child])
            _get_tree_edges_acc(tt, child, acc)
    return acc
