""" Tests the general GAC implementation on a nonogram example """
import unittest

from src.algorithms.gac.gac import GAC
from src.puzzles.nonogram.nonogram_constraint import NonogramConstraint


class TestGACOnNonogram(unittest.TestCase):
    """ GAC test with nonogram example """
    def setUp(self):

        self.variables = ['a', 'b', 'c', 'd']

        self.constraints = [
            NonogramConstraint('a [0] == c [0]'),
            NonogramConstraint('a [1] == d [0]'),
            NonogramConstraint('b [0] == c [1]'),
            NonogramConstraint('b [1] == d [1]')
        ]

        self.domains = {
            'a': ['01', '10', '00', '11'],
            'b': ['10'],
            'c': ['01'],
            'd': ['10']
        }

        self.solution = {
            'a': ['01'],
            'b': ['10'],
            'c': ['01'],
            'd': ['10']
        }

        self.gac = GAC()

        self.gac.initialize(self.domains, self.constraints)

    def test_solve(self):
        """ Checks that domain filtering reduces the domain """
        results = self.gac.domain_filtering()
        self.assertTrue(results)
        self.assertEqual(self.domains, self.solution)

if __name__ == '__main__':
    unittest.main()
