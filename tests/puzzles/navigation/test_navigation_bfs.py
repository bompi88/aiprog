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
        self.solutions = [19, 33, 39, 19, 23, 59]

        base_path = res.maps.__path__[0]

        maps = ['/ex0.txt', '/ex1.txt', '/ex2.txt',
                '/ex3.txt', '/ex4.txt', '/ex5.txt']

        self.tasks = []
        for _map in maps:
            path = base_path + _map
            grid = NavigationGrid(Map(open(path, 'r').read().splitlines()))
            self.tasks.append(grid)

        self.navigations = []
        for task in self.tasks:
            self.navigations.append(Navigation(task))

    def tearDown(self):
        from src.utils.id_generator import ID_GENERATOR
        ID_GENERATOR.ids = {}
        ID_GENERATOR.next_id = 1

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
