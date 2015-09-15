""" Navigation specialization of A* """
from src.algorithms.astar.best_first_search import BestFirstSearch
from src.algorithms.astar\
    .vertex_coloring.vertex_coloring_state import VertexColoringState
from src.modules.module2.utils.graph_reader import GraphReader
from src.algorithms.gac.gac import GAC


class VertexColoring(BestFirstSearch):
    """ Map navigation version of A* """

    def __init__(self, start, gui=None):
        BestFirstSearch.__init__(self, start, gui)

    def create_root_node(self):
        root = VertexColoringState(self.start)

        gac = GAC(root) # TODO fix
        # gac.initialize()
        # gac.domain_filtering()

        return root

    def arc_cost(self, a, b):
        return 0.5

def main():
    """ Text-based test of VertexColoring """
    solution = VertexColoring(GraphReader(
        GraphReader.parse_graph(GraphReader.read_graph('graph-color-1.txt'))
    )).best_first_search()

    if not solution:
        print "Failed"

if __name__ == '__main__':
    main()
