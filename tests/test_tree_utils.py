from unittest import TestCase
import treelib as tree

from context import get_tree_edges


class Test(TestCase):

    def test_get_tree_edges(self):
        test = tree.Tree()
        test.create_node("Harry", 1)  # root node
        test.create_node("Jane", 2, parent=1)
        test.create_node("Bill", 3, parent=1)
        test.create_node("Diane", 4, parent=2)
        test.create_node("Mary", 5, parent=4)
        test.create_node("Mark", 6, parent=2)

        # Should be:
        # [ [1, 2], [2, 4], [4, 5], [2, 6], [1, 3] ]
        edges = get_tree_edges(test)
        self.assertEqual(edges, [[1, 2], [2, 4], [4, 5], [2, 6], [1, 3]])
