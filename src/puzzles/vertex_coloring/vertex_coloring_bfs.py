""" Navigation specialization of A* """
from src.algorithms.astar.best_first_search import BestFirstSearch
from src.puzzles.\
    vertex_coloring.vertex_coloring_state import VertexColoringState
from src.algorithms.gac.gac import GAC


class VertexColoringBfs(BestFirstSearch):
    """ Map navigation version of A* """

    def __init__(self, start, gui=None, num_colors=None):
        BestFirstSearch.__init__(self, start, gui)

        self.gac = GAC()
        self.num_colors = num_colors or gui.num_colors

    def create_root_node(self):
        root = VertexColoringState(self.start, self.gac, self.num_colors)

        self.gac.initialize(root.domains, root.state.constraints)
        self.gac.domain_filtering()

        return root

    def arc_cost(self, a, b):
        return 0


def main():
    """ Text-based test of VertexColoring """
    import res.graphs
    from src.utils.const import C
    from src.puzzles.vertex_coloring.graph import Graph

    colors = 4
    path = res.graphs.__path__[0] + '/graph-color-2.txt'
    search = VertexColoringBfs(
        Graph(open(path, 'r').read().splitlines()),
        None, colors
    )

    search.verbosity = C.verbosity.VERBOSE
    solution = search.best_first_search()

    if not solution:
        print "Failed"

if __name__ == '__main__':
    main()
