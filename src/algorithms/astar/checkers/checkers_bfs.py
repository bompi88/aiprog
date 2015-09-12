""" Runnable script for solving 25-Checkers """
from src.algorithms.astar.best_first_search import BestFirstSearch
from src.algorithms.astar.checkers.checkers_state import CheckersState


class Checkers(BestFirstSearch):
    """ Implement the Checkers specialization of A* """

    def __init__(self, board):
        BestFirstSearch.__init__(self, board)

    def create_root_node(self):
        return CheckersState(self.start)

    def arc_cost(self, a, b):
        return 0.2

    @staticmethod
    def default_task():
        """ Return the board given as an example in the documentation """
        return [[7, 24, 10, 19, 3], [12, 20, 8, 22, 23], [2, 15, 25, 18, 13],
                [11, 21, 5, 9, 16], [17, 4, 14, 1, 6]]

def main():
    """ Run the basic example and print solution path """
    solution = Checkers(Checkers.default_task()).best_first_search()
    solution.print_path()

if __name__ == '__main__':
    main()
