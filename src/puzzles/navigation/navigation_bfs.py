""" Navigation specialization of A* """
from src.algorithms.astar.best_first_search import BestFirstSearch
from src.puzzles.navigation.navigation_state import NavigationState
from src.puzzles.navigation.navigation_grid import NavigationGrid
from src.puzzles.navigation.map import Map


class Navigation(BestFirstSearch):
    """ Map navigation version of A* """

    def __init__(self, start, gui=None):
        self.diagonal = gui.diagonal
        BestFirstSearch.__init__(self, start, gui, True)

    def create_root_node(self):
        return NavigationState(self.start, self.diagonal)

    def arc_cost(self, a, b):
        return 0.5


def main():
    """ Text-based test of Navigation """
    import res.maps
    path = res.maps.__path__[0] + '/ex7.txt'
    grid = NavigationGrid(Map(open(path, 'r').read().splitlines()))
    solution = Navigation(grid).best_first_search()

    solution.print_level()
    if not solution:
        print "Failed"

if __name__ == '__main__':
    main()
