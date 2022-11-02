import search
import unittest

test = {'A': {'B': 2, 'C': 5},
        'B': {'A': 2, 'C': 2, 'D': 4},
        'C': {'A': 5, 'B': 2, 'D': 5},
        'D': {'B': 4, 'C': 5, 'E': 2},
        'E': {'C': 5, 'D': 2}
        }

test2 = {'A': {'B': 2},
         'B': {'A': 2},
         'C': {}
         }


class TestDijkstra(unittest.TestCase):
    def setUp(self):
        self.test_function = search.dijkstra

    def test_path_true(self):
        self.assertEqual(self.test_function(test, 'A', 'D'), ['A', 'B', 'D'])

    def test_illegal_stop(self):
        self.assertRaises(BaseException, self.test_function, test, 'A', 'N')

    def test_illegal_start(self):
        self.assertRaises(BaseException, self.test_function, test, 'N', 'A')

    def test_no_path(self):
        self.assertRaises(BaseException, self.test_function, test2, 'A', 'C')


class TestDijkstraQueue(TestDijkstra):
    def setUp(self):
        self.test_function = search.dijkstra_queue


class TestAstar(TestDijkstra):
    def setUp(self):
        self.test_function = search.a_star
