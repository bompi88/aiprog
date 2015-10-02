from src.algorithms.puzzles\
    .vertex_coloring.vertex_coloring_bfs import VertexColoring
from src.modules.module2.utils.graph_reader import GraphReader
from src.modules.module2.utils.const import C


class StatusMock(object):
    def emit(self, str):
        print(str)


class GuiMock(object):
    def __init__(self):
        self.num_colors = 4
        self.mode = C.A_STAR
        self.delay = 0
        self.status_message = StatusMock()

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
