""" A Widget for drawing Graph states """
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal

from src.algorithms.puzzles.nonogram.nonogram_bfs import Nonogram
from src.modules.module3.utils.const import C
from src.modules.module3.utils.search_worker import SearchWorker


class NonogramGUI(QtGui.QFrame):
    """ Implement QFrame, which is a subclass of QWidget """
    status_message = pyqtSignal(str)

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)

        self.dx = self.dy = 20
        # self.offset_dx = self.offset_dy = 35
        self.graph_width_px = self.graph_height_px = 600
        # self.nc_adjust_x = 0 # Adjustment for negative coordinates
        # self.nc_adjust_y = 0
        # self.vertex_radii = 5
        # self.corners = []

        self.nonogram = None
        self.node = None
        self.delay = 50
        self.mode = C.A_STAR
        self.thread = SearchWorker()
        self.init_ui()

    def init_ui(self):
        """ Initialize the UI """
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def level_loaded(self, filename, nonogram):
        """ Called whenever a level is loaded, adjust Widget size """
        self.nonogram = nonogram

        print('level loaded')
        # self.node = VertexColoringState(graph)

        self.dx = self.dy = 20
        self.offset_dx = self.offset_dy = 35

        width_orig = (self.nonogram.x * self.dx)
        height_orig = (self.nonogram.y * self.dy)

        self.dx = self.dx * (self.graph_width_px / width_orig)
        width = (self.nonogram.x * self.dx)

        self.dy = self.dy * (self.graph_height_px / height_orig)
        height = self.nonogram.y * self.dy


        #width = self.dx * self.nonogram.x
        #height = self.dy * self.nonogram.y

        self.setMinimumSize(QtCore.QSize(width, height))
        self.parent().adjustSize()
        self.parent().resize(self.graph_width_px, self.parent().height())
        self.parent().setWindowTitle('Module 2 - A*-GAC - {}'.format(filename))
        self.update()
        self.status_message.emit(str('Loaded: {}'.format(filename)))

    def start_search(self):
        """ Start the search in the worker thread """
        # TODO fix
        vertex_search = Nonogram(self.nonogram, self)

        self.status_message.emit(str('Search started'))
        # self.thread.search(self, vertex_search)

    def paint(self, node):
        """ Receives a node and tells Qt to update the graphics """
        # self.nonogram = node.state

        self.nonogram = node
        # self.node = node
        self.update()

    def paintEvent(self, _): # pylint: disable=invalid-name
        """ Called by the Qt event loop when the widget should be updated """
        if self.nonogram is None:
            return

        painter = QtGui.QPainter(self)
        self.draw_nonogram(painter)
        print('paint event')

    def draw_nonogram(self, painter):
        colors = {
            1: QtGui.QColor(255, 0, 150),
            0: QtGui.QColor(255, 255, 150)
        }

        for y, row in enumerate(self.nonogram.solution):
            for x, element in enumerate(row):
                painter.setBrush(colors[element])
                painter.drawRect((x * self.dx), (y * self.dy), self.dx - 1, self.dy - 1)

    def set_graph(self, graph_read):
        filename, graph = graph_read

        self.level_loaded(filename, graph)

    def set_delay(self, delay):
        """ Change delay """
        self.delay = delay
        return True

    def set_opened_closed(self, opened, closed):
        self.opened = opened
        self.closed = closed
