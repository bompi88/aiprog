""" Navigation specialization of A* """
from src.algorithms.astar.best_first_search import BestFirstSearch
from src.algorithms.astar.navigation.navigation_state import NavigationState
from src.algorithms.astar.navigation.navigation_grid import NavigationGrid
from src.modules.module1.utils.map_reader import MapReader


class Navigation(BestFirstSearch):
    """ Map navigation version of A* """

    def __init__(self, start, gui=None):
        BestFirstSearch.__init__(self, start, gui)

    def create_root_node(self):
        return NavigationState(self.start)

    def arc_cost(self, a, b):
        return 0.5

def main():
    """ Text-based test of Navigation """
    solution = Navigation(
        NavigationGrid(MapReader(MapReader.read_map('ex_simple.txt')))
    ).best_first_search()

    if not solution:
        print "Failed"

if __name__ == '__main__':
    main()
