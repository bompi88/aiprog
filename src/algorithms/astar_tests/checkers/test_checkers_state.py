""" Unit tests for checkers state """
import unittest

from src.algorithms.puzzles.checkers.checkers_bfs import Checkers
from src.algorithms.puzzles.checkers.checkers_state import CheckersState


class TestCheckersState(unittest.TestCase):
    """ Tests various scenarios of checker states """

    def setUp(self):
        self.task = Checkers.default_task()

        self.test_state = CheckersState(self.task)

    def test_id_set_correctly(self):
        """ Test that id is set as intended """
        correct_id = ''.join([str(item) for row in self.task for item in row])

        self.assertEqual(correct_id, self.test_state.sid)

    def test_heuristic_evaluation(self):
        """ Test that heuristic evaluation for the default task is correct"""
        correct_h = 43

        self.assertEqual(correct_h, self.test_state.heuristic_evaluation())

    def test_generate_all_successors(self):
        """ Check that we get the correct number of successors """
        correct_length = 40

        successors = self.test_state.generate_all_successors()

        self.assertEqual(correct_length, len(successors))

    def test_is_solution(self):
        """ Test a solution state and non-solution state """
        solution = [[x + 5*y for x in range(1, 6)] for y in range(5)]

        state = CheckersState(solution)
        state.h = state.heuristic_evaluation()

        self.assertTrue(state.is_solution())
        self.assertFalse(self.test_state.is_solution())

    def test_manhattan_distance(self):
        """ Test the implementation of manhattan distance """
        a = (0, 0)
        b = (10, 10)
        res = 20
        self.assertEqual(CheckersState.manhattan_distance(a, b), res)

        a = (20, 0)
        self.assertEqual(CheckersState.manhattan_distance(a, b), res)

        a = (10, 0)
        res = 10
        self.assertEqual(CheckersState.manhattan_distance(a, b), res)

        a = (20, 20)
        res = 20
        self.assertEqual(CheckersState.manhattan_distance(a, b), res)

        a = (11, 10)
        res = 1
        self.assertEqual(CheckersState.manhattan_distance(a, b), res)

if __name__ == '__main__':
    unittest.main()
