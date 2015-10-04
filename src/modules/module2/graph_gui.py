""" A Widget for drawing Graph states """
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal

import res.graphs
from src.utils.const import C
from src.utils.search_worker import SearchWorker
from src.puzzles.vertex_coloring.graph import Graph
from src.puzzles.vertex_coloring.vertex_coloring_bfs import VertexColoringBfs
from src.puzzles.vertex_coloring.\
    vertex_coloring_state import VertexColoringState


class GraphGUI(QtGui.QFrame):
    # pylint: disable=too-many-instance-attributes
    """ Implement QFrame, which is a subclass of QWidget """
    status_message = pyqtSignal(str)

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)

        self.dx = self.dy = -1
        self.graph_width_px = self.graph_height_px = 600
        self.nc_adjust_x = 0 # Adjustment for negative coordinates
        self.nc_adjust_y = 0
        self.total_height = 0
        self.vertex_radii = 5

        self.num_colors = 4
        self.delay = 50
        self.vertex_numbering = False
        self.node = None
        self.set_graph(True)
        self.mode = C.search_mode.A_STAR
        self.thread = SearchWorker(self)
        self.init_ui()

    def init_ui(self):
        """ Initialize the UI """
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        size = QtCore.QSize(self.graph_width_px, self.graph_height_px)
        self.setMinimumSize(size)
        self.parent().adjustSize()

    def level_loaded(self, graph):
        """ Called whenever a level is loaded, adjust Widget size """
        self.node = VertexColoringState(graph, None, self.num_colors)

        self.nc_adjust_x = self.nc_adjust_y = 0

        width_orig = self.node.state.width
        height_orig = self.node.state.height

        self.dx = self.graph_width_px / float(width_orig)
        self.dy = self.graph_height_px / float(height_orig)

        self.nc_adjust_x = self.node.state.min_x * self.dx
        self.nc_adjust_y = self.node.state.min_y * self.dy

    def start_search(self):
        """ Start the search in the worker thread """
        self.status_message.emit(str('Search started'))
        self.thread.search(VertexColoringBfs(self.node.state, self))

    def set_solution(self, solution):
        self.node = VertexColoringState(
            solution.state,
            None,
            self.num_colors,
            solution.domains,
            solution.solution_length
        )

    def paint(self, node):
        """ Receives a node and tells Qt to update the graphics """
        self.graph = node.state
        self.node = node
        self.update()

    def paintEvent(self, _): # pylint: disable=invalid-name
        """ Called by the Qt event loop when the widget should be updated """
        if self.node is None:
            return

        painter = QtGui.QPainter(self)
        self.paint_graph(painter)

    def draw_vertex(self, vertex, painter, whites=False):
        """ Draws a vertex, either all the white nodes (with a domain length
        larger than 1) or all the colored nodes. Also draws optional
        vertex numbers. """
        x = (vertex[1] * self.dx) - self.nc_adjust_x
        y = (vertex[2] * self.dy) - self.nc_adjust_y
        y = self.graph_height_px - y
        point = QtCore.QPoint(x, y)

        colors = {
            C.graph_colors.RED: QtGui.QColor(255, 128, 0),
            C.graph_colors.GREEN: QtGui.QColor(0, 200, 0),
            C.graph_colors.BLUE: QtGui.QColor(0, 0, 255),
            C.graph_colors.ORANGE: QtGui.QColor(175, 0, 100),
            C.graph_colors.WHITE: QtGui.QColor(255, 255, 255),
            C.graph_colors.BLACK: QtGui.QColor(0, 0, 0),
            C.graph_colors.PINK: QtGui.QColor(255, 20, 147),
            C.graph_colors.YELLOW: QtGui.QColor(255, 255, 0),
            C.graph_colors.PURPLE: QtGui.QColor(238, 130, 238),
            C.graph_colors.BROWN: QtGui.QColor(222, 184, 135)
        }
        vertex_color = self.node.vertex_color(vertex[0])
        color = colors[vertex_color]

        painter.setPen(color)
        painter.setBrush(color)

        if whites and vertex_color is C.graph_colors.WHITE:
            painter.drawEllipse(point, self.vertex_radii, self.vertex_radii)
        elif not whites and not vertex_color is C.graph_colors.WHITE:
            painter.drawEllipse(point, self.vertex_radii, self.vertex_radii)

        if whites and self.vertex_numbering:
            painter.setPen(colors[C.graph_colors.BLACK])
            painter.drawText(x, y, str(vertex[0]))

    def draw_edge(self, edge, painter):
        """ Draws edge between two vertices """
        v1 = self.node.state.vertices[edge[0]]
        v2 = self.node.state.vertices[edge[1]]

        x1 = (v1[1] * self.dx) - self.nc_adjust_x
        y1 = (v1[2] * self.dy) - self.nc_adjust_y
        x2 = (v2[1] * self.dx) - self.nc_adjust_x
        y2 = (v2[2] * self.dy) - self.nc_adjust_y

        y1, y2 = self.graph_height_px - y1, self.graph_height_px - y2

        p1, p2 = QtCore.QPoint(x1, y1), QtCore.QPoint(x2, y2)

        painter.setPen(QtGui.QColor(120, 120, 120))
        painter.drawLine(p1, p2)

    def paint_graph(self, painter):
        """ The graph is painted by edges, unset and lastly colored vertices """
        for edge in self.node.state.edges:
            self.draw_edge(edge, painter)

        # Draw white vertices first
        for vertex in self.node.state.vertices:
            self.draw_vertex(vertex, painter, True)

        for vertex in reversed(self.node.state.vertices):
            self.draw_vertex(vertex, painter)

    def set_graph(self, default=False):
        """ Load level with a QFileDialog """
        folder = res.graphs.__path__[0]
        if default:
            path = folder + '/graph-color-1.txt'
        else:
            path = QtGui.QFileDialog.getOpenFileName(
                self.window(), "Open graph file", folder, "Text files (*.txt)"
            )
            if not path:
                return

        graph = Graph(open(path, 'r').read().splitlines())

        self.level_loaded(graph)

        filename = path.split('/')[-1]
        self.parent().setWindowTitle('Module 2 - A*-GAC - {}'.format(filename))
        self.status_message.emit(str('Loaded: {}'.format(filename)))
        self.update()

    def set_color(self, colors):
        """ Change color """
        self.num_colors = colors
        return True

    def set_vertex_numbering(self, numbering):
        self.vertex_numbering = numbering
        self.update()
        return True

    def set_delay(self, delay):
        """ Change delay """
        self.delay = delay
        return True

    # Not needed in GraphGui
    def set_opened_closed(self, opened, closed):
        pass
