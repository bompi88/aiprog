__author__ = 'krisvage'

import unittest
from algorithms.astar.checkers_bfs import Checkers

class TestCheckers(unittest.TestCase):
    def setUp(self):
        self.solution = [
            [ 1,  2,  3,  4,  5],
            [ 6,  7,  8,  9, 10],
            [11, 12, 13, 14, 15],
            [16, 17, 18, 19, 20],
            [21, 22, 23, 24, 25]
        ]

        self.task = [
            [  7, 24, 10, 19,  3],
            [ 12, 20,  8, 22, 23],
            [  2, 15, 25, 18, 13],
            [ 11, 21,  5,  9, 16],
            [ 17,  4, 14,  1,  6]
        ]

        self.checker = Checkers(self.task)

    def test_solve(self):
        proposal_state = self.checker.solve()
        proposal = proposal_state.state

        for i, list in enumerate(self.solution):
            for j, element in enumerate(list):
                self.assertEqual(element, proposal[i][j])

if __name__ == '__main__':
    unittest.main()