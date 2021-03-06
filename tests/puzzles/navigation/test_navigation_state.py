""" Tests methods on NavigationState """
import unittest

from src.puzzles.navigation.navigation_bfs import NavigationBfs
from src.puzzles.navigation.navigation_state import NavigationState
from src.puzzles.navigation.map import Map
from src.utils.const import C
import res.maps.extras


class TestNavigationState(unittest.TestCase):
    """ Performs tests on NavigationState """
    def setUp(self):
        path = res.maps.extras.__path__[0] + '/ex_simple.txt'
        self.task = Map(open(path, 'r').read().splitlines())

        self.test_state = NavigationState(self.task)

    def test_id_set_correctly(self):
        """ Test that id is set as intended """
        correct_id = 1

        self.assertEqual(correct_id, self.test_state.sid)

        next_id = 2
        for i, x in enumerate(self.test_state.generate_all_successors()):
            self.assertEqual(next_id + i, x.sid)

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

        search = NavigationBfs(self.task)
        search.verbosity = C.verbosity.TEST
        solution_state = search.best_first_search()

        self.assertTrue(solution_state.is_solution())

if __name__ == '__main__':
    unittest.main()
