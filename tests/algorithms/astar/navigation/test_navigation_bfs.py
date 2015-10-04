""" Tests navigation search with correct solutions """
import unittest

from src.puzzles.navigation.navigation_bfs import Navigation
from src.puzzles.navigation.navigation_grid import NavigationGrid
from src.puzzles.navigation.map import MapReader


class TestNavigation(unittest.TestCase):
    """ Test cases for navigation """
    # pylint: disable=too-many-instance-attributes

    def setUp(self):
        self.solution_task_1 = 10
        self.solution_task_2 = 19
        self.solution_task_3 = 33
        self.solution_task_4 = 39
        self.solution_task_5 = 19
        self.solution_task_6 = 23
        self.solution_task_7 = 59
        self.solution_task_8 = 38
        self.solution_task_9 = 54

        self.task_1 = NavigationGrid(
            MapReader(MapReader.read_map('ex_simple.txt'))
        )
        self.task_2 = NavigationGrid(MapReader(MapReader.read_map('ex0.txt')))
        self.task_3 = NavigationGrid(MapReader(MapReader.read_map('ex1.txt')))
        self.task_4 = NavigationGrid(MapReader(MapReader.read_map('ex2.txt')))
        self.task_5 = NavigationGrid(MapReader(MapReader.read_map('ex3.txt')))
        self.task_6 = NavigationGrid(MapReader(MapReader.read_map('ex4.txt')))
        self.task_7 = NavigationGrid(MapReader(MapReader.read_map('ex5.txt')))
        self.task_8 = NavigationGrid(MapReader(MapReader.read_map('ex6.txt')))
        self.task_9 = NavigationGrid(MapReader(MapReader.read_map('ex7.txt')))

        self.navigation_1 = Navigation(self.task_1)
        self.navigation_2 = Navigation(self.task_2)
        self.navigation_3 = Navigation(self.task_3)
        self.navigation_4 = Navigation(self.task_4)
        self.navigation_5 = Navigation(self.task_5)
        self.navigation_6 = Navigation(self.task_6)
        self.navigation_7 = Navigation(self.task_7)
        self.navigation_8 = Navigation(self.task_8)
        self.navigation_9 = Navigation(self.task_9)

    def test_solve(self):
        """ Runs searches and asserts expected results """
        proposal_state_task_1 = self.navigation_1.best_first_search()
        proposal_state_task_2 = self.navigation_2.best_first_search()
        proposal_state_task_3 = self.navigation_3.best_first_search()
        proposal_state_task_4 = self.navigation_4.best_first_search()
        proposal_state_task_5 = self.navigation_5.best_first_search()
        proposal_state_task_6 = self.navigation_6.best_first_search()
        proposal_state_task_7 = self.navigation_7.best_first_search()
        proposal_state_task_8 = self.navigation_8.best_first_search()
        proposal_state_task_9 = self.navigation_9.best_first_search()

        # Check if number of steps taken equals the solution
        self.assertEqual(proposal_state_task_1.solution_length(),
                         self.solution_task_1)
        self.assertEqual(proposal_state_task_2.solution_length(),
                         self.solution_task_2)
        self.assertEqual(proposal_state_task_3.solution_length(),
                         self.solution_task_3)
        self.assertEqual(proposal_state_task_4.solution_length(),
                         self.solution_task_4)
        self.assertEqual(proposal_state_task_5.solution_length(),
                         self.solution_task_5)
        self.assertEqual(proposal_state_task_6.solution_length(),
                         self.solution_task_6)
        self.assertEqual(proposal_state_task_7.solution_length(),
                         self.solution_task_7)
        self.assertEqual(proposal_state_task_8.solution_length(),
                         self.solution_task_8)
        self.assertEqual(proposal_state_task_9.solution_length(),
                         self.solution_task_9)

if __name__ == '__main__':
    unittest.main()
