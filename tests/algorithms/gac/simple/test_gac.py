import unittest
from src.algorithms.gac.gac import GAC
from tests.algorithms.gac.simple.simple_constraint import SimpleConstraint


class TestGAC(unittest.TestCase):
    def setUp(self):
        variables = ['a', 'b', 'c']
        self.constraints = [
            SimpleConstraint('a != b', variables),
            SimpleConstraint('a != c', variables),
            SimpleConstraint('b != c', variables),
            SimpleConstraint('a == 2', variables),
            SimpleConstraint('b == 1', variables),
        ]

        self.domains = {
            'a': [0, 1, 2],
            'b': [0, 1, 2],
            'c': [0, 1, 2]
        }

        self.solution = {
            'a': [2],
            'c': [0],
            'b': [1],
        }

        self.gac = GAC()
        self.gac.initialize(self.domains, self.constraints)

    def test_solve(self):
        results = self.gac.domain_filtering()
        self.assertTrue(results)
        self.assertEqual(self.domains, self.solution)

if __name__ == '__main__':
    unittest.main()
