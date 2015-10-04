""" Tests navigation search with correct solutions """
import unittest

from src.puzzles.navigation.navigation_bfs import Navigation
from src.puzzles.navigation.navigation_grid import NavigationGrid
from src.puzzles.navigation.map import Map
from src.utils.const import C
import res.maps


class TestNavigation(unittest.TestCase):
    """ Test cases for navigation """
    # pylint: disable=too-many-instance-attributes

    def setUp(self):
        self.solutions = [10, 19, 33, 39, 19, 23, 59, 38, 54]

        base_path = res.maps.__path__[0]

        maps = ['/ex_simple.txt', '/ex0.txt', '/ex1.txt', '/ex2.txt',
                '/ex3.txt', '/ex4.txt', '/ex5.txt', '/ex6.txt', '/ex7.txt']

        self.tasks = []
        for map in maps:
            path = base_path + map
            grid = NavigationGrid(Map(open(path, 'r').read().splitlines()))
            self.tasks.append(grid)

        self.navigations = []
        for task in self.tasks:
            self.navigations.append(Navigation(task))

    def test_solve(self):
        """ Runs searches and asserts expected results """
        proposals = []
        for navigation in self.navigations:
            navigation.verbosity = C.verbosity.TEST
            proposals.append(navigation.best_first_search())

        # Check if number of steps taken equals the solution
        for i, proposal in enumerate(proposals):
            self.assertEqual(proposal.solution_length(), self.solutions[i])


if __name__ == '__main__':
    unittest.main()
