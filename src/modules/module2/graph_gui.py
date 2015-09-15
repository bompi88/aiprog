""" A Widget for drawing Graph states """
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal
from src.modules.module2.utils.const import C
from src.modules.module2.utils.search_worker import SearchWorker
from src.algorithms.astar.\
    vertex_coloring.vertex_coloring_bfs import VertexColoring
from src.algorithms.astar.\
    vertex_coloring.vertex_coloring_state import VertexColoringState

class GraphGUI(QtGui.QFrame):
    """ Implement QFrame, which is a subclass of QWidget """
    status_message = pyqtSignal(str)

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)

        self.dx = self.dy = 20
        self.offset_dx = self.offset_dy = 35
        self.graph_width_px = self.graph_height_px = 600
        self.nc_adjust_x = 0 # Adjustment for negative coordinates
        self.nc_adjust_y = 0
        self.vertex_radii = 5
        self.corners = []

        self.graph = None
        self.node = None
        self.delay = 50
        self.mode = C.A_STAR
        self.thread = SearchWorker()
        self.init_ui()

    def init_ui(self):
        """ Initialize the UI """
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def level_loaded(self, filename, graph):
        """ Called whenever a level is loaded, adjust Widget size """
        self.graph = graph
        self.node = VertexColoringState(graph, None)

        self.dx = self.dy = 20
        self.offset_dx = self.offset_dy = 35
        self.nc_adjust_x = self.nc_adjust_y = 0

        width_orig = (self.graph.width * self.dx) + (2 * self.offset_dx)
        height_orig = (self.graph.height * self.dy) + (2 * self.offset_dy)

        self.dx = self.dx * (self.graph_width_px / width_orig)
        width = (self.graph.width * self.dx) + (2 * self.offset_dx)

        self.dy = self.dy * (self.graph_height_px / height_orig)
        height = (self.graph.height * self.dy) + (2 * self.offset_dy)

        self.nc_adjust_x = self.graph.min_x * self.dx
        self.nc_adjust_y = self.graph.min_y * self.dy

        c1x, c2x = self.offset_dx, int(width) - self.offset_dx
        c1y, c2y = self.offset_dy, int(height) - self.offset_dy

        self.corners = [[c1x, c1y], [c2x, c1y], [c1x, c2y], [c2x, c2y]]

        self.setMinimumSize(QtCore.QSize(width, height))
        self.parent().adjustSize()
        self.parent().resize(self.graph_width_px, self.parent().height())
        self.parent().setWindowTitle('Module 2 - A*-GAC - {}'.format(filename))
        self.update()
        self.status_message.emit(str('Loaded: {}'.format(filename)))

    def start_search(self):
        """ Start the search in the worker thread """
        vertex_search = VertexColoring(self.graph, self)

        self.status_message.emit(str('Search started'))
        self.thread.search(self, vertex_search)

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

    def draw_vertex(self, vertex, painter):
        x = (vertex[1] * self.dx) + self.offset_dx - self.nc_adjust_x
        y = (vertex[2] * self.dy) + self.offset_dy - self.nc_adjust_y
        point = QtCore.QPoint(x, y)

        color = {
            C.RED: QtGui.QColor(255, 128, 0),
            C.GREEN: QtGui.QColor(0, 200, 0),
            C.BLUE: QtGui.QColor(0, 0, 255),
            C.ORANGE: QtGui.QColor(175, 0, 100),
            C.WHITE: QtGui.QColor(255, 255, 255),
            C.BLACK: QtGui.QColor(0, 0, 0)
        }[self.node.vertex_color(vertex[0])]

        painter.setPen(color)
        painter.setBrush(color)
        painter.drawEllipse(point, self.vertex_radii, self.vertex_radii)

    def draw_edge(self, edge, painter):
        v1, v2 = self.graph.vertices[edge[0]], self.graph.vertices[edge[1]]

        x1 = (v1[1] * self.dx) + self.offset_dx - self.nc_adjust_x
        y1 = (v1[2] * self.dy) + self.offset_dy - self.nc_adjust_y
        x2 = (v2[1] * self.dx) + self.offset_dx - self.nc_adjust_x
        y2 = (v2[2] * self.dy) + self.offset_dy - self.nc_adjust_y

        p1, p2 = QtCore.QPoint(x1, y1), QtCore.QPoint(x2, y2)

        painter.setPen(QtGui.QColor(120, 120, 120))
        painter.drawLine(p1, p2)

    def draw_corners(self, painter):
        for i, corner1 in enumerate(self.corners):
            for j, corner2 in enumerate(self.corners):
                x1, y1 = corner1
                x2, y2 = corner2

                if i == j or (x1 != x2 and y1 != y2):
                    continue

                p1, p2 = QtCore.QPoint(x1, y1), QtCore.QPoint(x2, y2)

                painter.setPen(QtGui.QColor(255, 255, 150))
                painter.drawLine(p1, p2)

    def paint_graph(self, painter):
        """ Called by the paintEvent, we iterate over the map and draw tiles """
        self.draw_corners(painter)

        for edge in self.graph.edges:
            self.draw_edge(edge, painter)

        for vertex in self.graph.vertices:
            self.draw_vertex(vertex, painter)

    def set_graph(self, graph_read):
        filename, graph = graph_read

        self.level_loaded(filename, graph)

    def set_delay(self, delay):
        """ Change delay """
        self.delay = delay
        return True
