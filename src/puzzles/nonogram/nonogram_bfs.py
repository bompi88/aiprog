""" Nonogram specialization of A* """
from src.algorithms.astar.best_first_search import BestFirstSearch
from src.puzzles.nonogram.nonogram_state import NonogramState
from src.algorithms.gac.gac import GAC


class NonogramBfs(BestFirstSearch):
    """ Nonogram version of A* """

    def __init__(self, start, gui=None):
        BestFirstSearch.__init__(self, start, gui)

        self.gac = GAC()

    def create_root_node(self):
        root = NonogramState(self.start, self.gac)

        self.gac.initialize(root.domains, root.state.constraints)
        self.gac.domain_filtering()

        return root

    def arc_cost(self, a, b):
        return 0.5


def main():
    """ Text-based test of nonogram """
    import res.nonograms
    from src.puzzles.nonogram.nonogram import Nonogram
    path = res.nonograms.__path__[0] + '/nono-heart-1.txt'
    nonogram = Nonogram(open(path, 'r').read().splitlines())
    solution = NonogramBfs(nonogram).best_first_search()

    if not solution:
        print "Failed"

if __name__ == '__main__':
    main()
