__author__ = 'bompi88'

import unittest
from algorithms.gac.gac import GAC


class TestGAC(unittest.TestCase):
    def setUp(self):

        self.variables = ['a', 'b', 'c', 'd', 'e']

        self.constraints = [
            'a > 1',
            'b < 1',
            'c == 0',
            'd != 0',
            'd != 2',
            'e == a',
            'a > b'  # This should also work and not fail :(
        ]

        self.domains = {
            'a': [ 0, 1, 2],
            'b': [ 0, 1, 2],
            'c': [ 0, 1, 2],
            'd': [ 0, 1, 2],
            'e': [ 0, 1, 2]
        }

        self.solution = {
            'a': [2],
            'c': [0],
            'b': [0],
            'd': [1],
            'e': [2]
        }

        self.gac = GAC()

        self.gac.initialize(self.variables, self.domains, self.constraints)

    def test_solve(self):
        results = self.gac.domain_filtering()
        print results
        self.assertEqual(results, self.solution)

if __name__ == '__main__':
    unittest.main()
