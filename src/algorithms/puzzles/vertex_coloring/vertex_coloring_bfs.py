""" Navigation specialization of A* """
from src.algorithms.astar.best_first_search import BestFirstSearch
from src.algorithms.puzzles.vertex_coloring.vertex_coloring_state import VertexColoringState
from src.algorithms.gac.gac import GAC


class VertexColoring(BestFirstSearch):
    """ Map navigation version of A* """

    def __init__(self, start, gui=None):
        BestFirstSearch.__init__(self, start, gui)

        self.gac = GAC()

    def create_root_node(self):
        root = VertexColoringState(self.start, self.gac, self.gui.num_colors)

        self.gac.initialize(root.domains, root.state.constraints)
        self.gac.domain_filtering()

        return root

    def arc_cost(self, a, b):
        return 0
