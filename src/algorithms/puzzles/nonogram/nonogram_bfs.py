""" Nonogram specialization of A* """
from src.algorithms.astar.best_first_search import BestFirstSearch
from src.algorithms.puzzles.nonogram.nonogram_state import NonogramState
from src.modules.module3.utils.nonogram_reader import NonogramReader
from src.algorithms.gac.gac import GAC


class Nonogram(BestFirstSearch):
    """ Nonogram version of A* """

    def __init__(self, start, gui=None):
        BestFirstSearch.__init__(self, start, gui)

        self.gac = GAC()

    def create_root_node(self):
        print 'root node'
        root = NonogramState(self.start, self.gac)
        print 'root node created'
        print 'FUCKK'
        print root.domains

        self.gac.initialize(root.state.variables, root.domains, root.state.constraints)
        self.gac.domain_filtering()

        print 'FUCKK'
        print root.domains

        return root

    def arc_cost(self, a, b):
        return 0.5


def main():
    """ Text-based test of nonogram """
    solution = Nonogram(NonogramReader(NonogramReader.parse_nonogram(
        NonogramReader.read_nonogram('nono-heart-1.txt')
    ))).best_first_search()

    if not solution:
        print "Failed"

if __name__ == '__main__':
    main()
