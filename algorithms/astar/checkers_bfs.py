__author__ = 'krisvage'

from best_first_search import BestFirstSearch
from checkers_state import CheckersState

class Checkers(BestFirstSearch):
    def __init__(self, board):
        BestFirstSearch.__init__(self, board);

    def solve(self):
        return self.best_first_search()

    def create_root_node(self):
        return CheckersState(self.start)

    def arc_cost(self, a, b):
        return 0.2

def main():
    task = [
        [  7, 24, 10, 19,  3],
        [ 12, 20,  8, 22, 23],
        [  2, 15, 25, 18, 13],
        [ 11, 21,  5,  9, 16],
        [ 17,  4, 14,  1,  6]
    ]

    checkers = Checkers(task)

    solution = checkers.best_first_search()
    solution.print_level()

if __name__ == '__main__':
    main()