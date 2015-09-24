import unittest
from src.algorithms.gac.gac import GAC


class TestGACOnNonogram(unittest.TestCase):
    def setUp(self):

        self.variables = ['a', 'b', 'c', 'd']

        self.constraints = [
            'a [0] == c [0]',
            'a [1] == d [0]',
            'b [0] == c [1]',
            'b [1] == d [1]'
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

        self.gac.initialize(self.variables, self.domains, self.constraints)

    def test_solve(self):
        results = self.gac.domain_filtering()
        self.assertEqual(results, self.solution)

if __name__ == '__main__':
    unittest.main()
