""" Test GAC on a vertex coloring example """
import unittest

from src.algorithms.gac.gac import GAC
from src.puzzles.vertex_coloring.vertex_constraint import VertexConstraint


class TestGACVertexColoring(unittest.TestCase):
    """ Test class for GAC and vertex coloring """
    def setUp(self):

        self.variables = ['v1', 'v2', 'v3', 'v4']

        self.constraints = [
            VertexConstraint('v1 != v2'),
            VertexConstraint('v2 != v3'),
            VertexConstraint('v3 != v4'),
            VertexConstraint('v4 != v1')
        ]

        self.domains = {
            'v1': [0],
            'v2': [0, 1],
            'v3': [0, 1],
            'v4': [0, 1]
        }

        self.solution = {
            'v1': [0],
            'v2': [1],
            'v3': [0],
            'v4': [1]
        }

        self.gac = GAC()

        self.gac.initialize(self.domains, self.constraints)

    def test_solve(self):
        """ Test that domain filtering solves an example with only one step """
        results = self.gac.domain_filtering()
        self.assertTrue(results)
        self.assertEqual(self.domains, self.solution)

if __name__ == '__main__':
    unittest.main()
