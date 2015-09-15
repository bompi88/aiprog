""" A Widget for drawing Navigation states """
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal

from src.modules.module1.utils.search_worker import SearchWorker
from src.modules.module1.utils.const import C
from src.algorithms.astar.navigation.navigation_bfs import Navigation
from src.algorithms.astar.navigation.navigation_grid import NavigationGrid
from src.algorithms.astar.navigation.navigation_state import NavigationState


class NavigationGUI(QtGui.QFrame):
    """ Implement QFrame, which is a subclass of QWidget """
    status_message = pyqtSignal(str)

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)

        self.dx = self.dy = 40

        self.node = None
        self.opened = None
        self.closed = None
        self.delay = 50
        self.mode = C.A_STAR
        self.thread = SearchWorker()
        self.init_ui()

    def init_ui(self):
        """ Initialize the UI """
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def level_loaded(self, filename, grid):
        """ Called whenever a level is loaded, adjust Widget size """
        self.node = NavigationState(grid)
        self.opened = None
        self.closed = None

        scaled_dim = (self.node.state.map.x_dim() // 10)
        x = self.node.state.map.x_dim() * (self.dx - (scaled_dim * 5))
        y = self.node.state.map.y_dim() * (self.dy - (scaled_dim * 5))
        self.setMinimumSize(QtCore.QSize(x, y))

        self.parent().adjustSize()
        self.parent().resize(600, self.parent().height())
        self.parent().setWindowTitle(
            'Module 1 - A* Navigation Problems - {}'.format(filename)
        )

        self.status_message.emit(str('Loaded: {}'.format(filename)))

    def start_search(self):
        """ Start the search in the worker thread """
        navigation = Navigation(
            NavigationGrid(self.node.state.map), self)

        self.status_message.emit(str('Search started'))
        self.thread.search(self, navigation)

    def set_opened_closed(self, opened, closed):
        self.opened = opened
        self.closed = closed

    def paint(self, node):
        """ Receives a node and tells Qt to update the graphics """
        self.node = node

        self.update()

    def paintEvent(self, _): # pylint: disable=invalid-name
        """ Called by the Qt event loop when the widget should be updated """
        if self.node is None:
            return

        painter = QtGui.QPainter(self)
        self.paint_map(painter)

    def is_visited(self, x, y):
        """ Checks whether (x,y) is visited in the current state """
        y_dim = self.node.state.map.y_dim()
        return self.node.state.is_visited([x, y_dim - y - 1])

    def is_on_frontier(self, x, y):
        if not self.opened:
            return False

        y_dim = self.node.state.map.y_dim()

        for node in self.opened:
            if type(node) is tuple:
                node = node[1] # Heapq for astar, normal list for BFS/DFS

            if [x, y_dim - y - 1] == node.state.last_visited():
                return True

        return False

    def is_closed(self, x, y):
        if not self.closed:
            return False

        y_dim = self.node.state.map.y_dim()

        for node in self.closed:
            if [x, y_dim - y - 1] == node.state.last_visited():
                return True

        return False

    def get_color(self, x, y, visited=False, frontier=False, closed=False):
        """ Return a QColor based on the tile and whether it is visited """

        if visited:
            color = {
                C.TILE:  QtGui.QColor(80, 80, 80),
                C.START: QtGui.QColor(153, 204, 255),
                C.GOAL:  QtGui.QColor(0, 255, 0)
            }[self.node.state.map.grid[y][x]]
        elif frontier:
            color = QtGui.QColor(255, 255, 80)
        elif closed:
            color = QtGui.QColor(210, 210, 210)
        else:
            color = {
                C.TILE:     QtGui.QColor(255, 255, 255),
                C.OBSTACLE: QtGui.QColor(255, 0, 0),
                C.START:    QtGui.QColor(0, 0, 255),
                C.GOAL:     QtGui.QColor(51, 102, 0)
            }[self.node.state.map.grid[y][x]]

        return color

    def draw(self, x, y, painter):
        """ Draws rectangles, either with a black border or without a border.
         If the tile is visited we draw a smaller rectangle on top.
        """
        color = self.get_color(x, y)

        dx = dy = self.dx - ((self.node.state.map.y_dim() // 10) * 5)

        if self.node.state.map.grid[y][x] is C.OBSTACLE:
            painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 1))
        else:
            painter.setPen(QtGui.QPen(color, 1))
        painter.setBrush(color)
        painter.drawRect((x * dx), (y * dy), dx - 1, dy - 1)

        is_visited = self.is_visited(x, y)
        is_on_frontier = self.is_on_frontier(x, y)
        is_closed = self.is_closed(x, y)
        if is_visited or is_on_frontier or is_closed:
            color = self.get_color(x, y, is_visited, is_on_frontier, is_closed)
            painter.setPen(QtGui.QPen(color, 1))
            painter.setBrush(color)
            painter.drawRect((x * dx) + 4, (y * dy) + 4, dx - 9, dy - 9)


    def paint_map(self, painter):
        """ Called by the paintEvent, we iterate over the map and draw tiles """
        for y in range(self.node.state.map.y_dim()):
            for x in range(self.node.state.map.x_dim()):
                self.draw(x, y, painter)

    def set_mode(self, mode):
        """ Chainable method for use in lambdas, change mode """
        self.mode = mode
        return True

    def set_delay(self, delay):
        """ Change delay """
        self.delay = delay
        return True
