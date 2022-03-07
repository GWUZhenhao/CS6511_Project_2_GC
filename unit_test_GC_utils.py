from unittest import TestCase
import numpy as np
from GC_utils import sortbyfreq, Vairables_iter, Node, CStree
from numpy import array


# Test the function of sorting by frequency
class Test_sortbyfreq(TestCase):

    def setUp(self):
        self.arr = [4, 5, 6, 7, 5, 6, 7, 6, 7, 7]

    def test_sortbyfreq(self):
        self.assertEqual(sortbyfreq(self.arr), [7, 6, 5, 4])

# Test the iteration class
class TestVairables_iter(TestCase):
    def setUp(self):
        # the variable with max degree is variable 2
        # All the variables has same color choice
        edges = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 6), (2, 7), (3, 5), (3, 6), (3, 7), (4, 5), (4, 6),
                 (4, 7), (5, 6), (5, 7), (6, 7)]
        state = {1: array([0., 1., 2., 3.]), 2: array([0., 1., 2., 3.]), 3: array([0., 1., 2., 3.]),
                 4: array([0., 1., 2., 3.]), 5: array([0., 1., 2., 3.]), 6: array([0., 1., 2., 3.]),
                 7: array([0., 1., 2., 3.])}
        self.iter = Vairables_iter(state=state, edges=edges)

    def test_next(self):
        self.assertEqual(next(iter(self.iter)), 2)

# Test the node class
class TestNode(TestCase):

    def setUp(self):
        self.state = {1: array([0., 1., 2., 3.]), 2: [0.0], 3: array([0., 1., 2., 3.]), 4: array([0., 1., 2., 3.]),
                      5: array([0., 1., 2., 3.]), 6: array([0., 1., 2., 3.]), 7: array([0., 1., 2., 3.])}
        self.edges = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 6), (2, 7), (3, 5), (3, 6), (3, 7), (4, 5),
                      (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)]
        self.node = Node(self.state, self.edges)

    # test the if ac_3 function can reduce state to target state
    def test_ac_3(self):
        target_state = {1: array([1., 2., 3.]), 2: [0.0], 3: array([1., 2., 3.]), 4: array([1., 2., 3.]),
                        5: array([0., 1., 2., 3.]), 6: array([1., 2., 3.]), 7: array([1., 2., 3.])}
        flag = True
        for variable in target_state:
            if not np.equal(target_state[variable], self.node.state[variable]).all():
                return False
        self.assertTrue(flag)

    def test_check_failed(self):
        self.assertFalse(self.node.check_failed())

    def test_can_expand(self):
        self.assertTrue(self.node.can_expand())

    def test_check_success(self):
        self.assertFalse(self.node.check_success())


# Test the constraint tree class
class TestCStree(TestCase):
    def setUp(self):
        self.edges = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 6), (2, 7), (3, 5), (3, 6), (3, 7), (4, 5), (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)]
        self.num_color = 4
        self.cstree = CStree(edges=self.edges, num_color=self.num_color)

    def test_expanding_tree(self):
        result_state = self.cstree.finished_node.state
        target_state = {1: 2.0, 2: 0.0, 3: 1.0, 4: 1.0, 5: 0.0, 6: 2.0, 7: 3.0}
        self.assertEqual(result_state, target_state)

    # method for visualization, need test by the actual human
    def test_visualization(self):
        self.cstree.visualization()