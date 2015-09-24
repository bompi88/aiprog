__author__ = 'bompi88'

import unittest

from src.algorithms.puzzles.navigation.navigation_bfs import Navigation
from src.algorithms.puzzles.navigation.navigation_state import NavigationState
from src.algorithms.puzzles.navigation.navigation_grid import NavigationGrid
from src.modules.module1.utils.map_reader import MapReader


class TestNavigationState(unittest.TestCase):

    def setUp(self):
        self.task = NavigationGrid(MapReader(MapReader.read_map('ex_simple.txt')))

        self.test_state = NavigationState(self.task)

    def test_id_set_correctly(self):
        """ Test that id is set as intended """
        correct_id = 1

        self.assertEqual(correct_id, self.test_state.sid)

    def test_heuristic_evaluation(self):
        """ Test that heuristic evaluation for the default task is correct"""
        correct_h = 6.4031242374328485

        self.assertEqual(correct_h, self.test_state.heuristic_evaluation())

    def test_generate_all_successors(self):
        """ Check that we get the correct number of successors """
        correct_length = 2

        successors = self.test_state.generate_all_successors()

        self.assertEqual(correct_length, len(successors))

    def test_is_solution(self):
        """ Test a solution state and non-solution state """

        self.assertFalse(self.test_state.is_solution())

        solution_state = Navigation(self.task).best_first_search()

        self.assertTrue(solution_state.is_solution())

if __name__ == '__main__':
    unittest.main()