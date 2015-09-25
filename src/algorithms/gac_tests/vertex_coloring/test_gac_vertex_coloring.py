import unittest
from src.algorithms.gac.gac import GAC


class TestGACVertexColoring(unittest.TestCase):
    def setUp(self):

        self.variables = ['v1', 'v2', 'v3', 'v4']

        self.constraints = [
            ('v1 != v2', 'v2 != v1'),
            ('v2 != v3', 'v3 != v2'),
            ('v3 != v4', 'v4 != v3'),
            ('v4 != v1', 'v1 != v4')
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

        self.gac.initialize(self.variables, self.domains, self.constraints)

    def test_solve(self):
        results = self.gac.domain_filtering()
        self.assertEqual(results, self.solution)

if __name__ == '__main__':
    unittest.main()
