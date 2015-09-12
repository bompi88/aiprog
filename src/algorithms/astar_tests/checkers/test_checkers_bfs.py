""" Unit tests for the 25-Checkers implementation of A* """
import unittest

from src.algorithms.astar.checkers.checkers_bfs import Checkers
from src.algorithms.astar.const import C


class TestCheckers(unittest.TestCase):
    """ Test checkers with the default task """

    def setUp(self):
        self.solution = [[x + 5*y for x in range(1, 6)] for y in range(5)]

        self.task = Checkers.default_task()

        self.checker = Checkers(self.task)
        self.checker.verbosity = C.TEST

    def test_search(self):
        """ More of a integration test, than unit test, check that the solution
         returned is a solved board
        """
        proposal_state = self.checker.best_first_search()
        proposal = proposal_state.state

        for i, row in enumerate(self.solution):
            for j, element in enumerate(row):
                self.assertEqual(element, proposal[i][j])

if __name__ == '__main__':
    unittest.main()
