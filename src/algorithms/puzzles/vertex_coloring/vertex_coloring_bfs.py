""" Navigation specialization of A* """
from src.algorithms.astar.best_first_search import BestFirstSearch
from src.algorithms.puzzles.vertex_coloring.vertex_coloring_state import VertexColoringState
from src.modules.module2.utils.graph_reader import GraphReader
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


class StatusMock(object):
    def emit(self, str):
        pass


class GuiMock(object):

    def __init__(self):
        self.num_colors = 4
        self.mode = 1 # TODO: C.A_STAR
        self.delay = 0
        self.status_message = StatusMock()

    def set_opened_closed(self, opened, closed):
        pass

    def paint(self, node):
        pass


def main():
    """ Text-based test of VertexColoring """
    solution = VertexColoring(
        GraphReader(GraphReader.parse_graph(
            GraphReader.read_graph('rand-50-4-color1.txt')
        )),
        GuiMock()
    ).best_first_search()

    if not solution:
        print "Failed"

if __name__ == '__main__':
    main()
