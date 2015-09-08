from algorithms.astar.best_first_search import BestFirstSearch
from algorithms.astar.navigation.navigation_state import NavigationState
from algorithms.astar.navigation.navigation_grid import NavigationGrid
from modules.module1.map_reader import MapReader
from algorithms.astar.navigation.const import *

class Navigation(BestFirstSearch):
    def __init__(self, board, gui=None):
        BestFirstSearch.__init__(self, board, gui);

    def solve(self):
        return self.best_first_search()

    def create_root_node(self):
        return NavigationState(self.start)

    def arc_cost(self, a, b):
        return const.ARC_COST

def main():
    map = MapReader('ex_simple.txt')

    navigation = Navigation(NavigationGrid(map))

    solution = navigation.best_first_search()
    if solution:
        solution.print_level()
    else:
        print("FAIL")

if __name__ == '__main__':
    main()