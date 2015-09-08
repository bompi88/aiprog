import sys

from PyQt4 import QtGui, QtCore

from algorithms.astar.navigation.navigation_grid import NavigationGrid
from algorithms.astar.navigation.navigation_bfs import Navigation
from search_worker import SearchWorker
from map_reader import MapReader
from algorithms.astar.navigation.const import *


class Module1(QtGui.QWidget):
    def __init__(self):
        super(Module1, self).__init__()

        self.board      = None
        self.node       = None
        self.filename   = None
        self.solved     = False
        self.dx = 20  # Pixels per tile in x-direction
        self.dy = 20  # Pixels per tile in y-direction
        self.offset_x = 50  # Offset from left
        self.offset_y = 50  # Offset from top

        self.thread = SearchWorker()

        self.load_level_button = QtGui.QPushButton('Load new level', self)
        QtCore.QObject.connect(self.load_level_button, QtCore.SIGNAL("clicked()"), self.load_level)

        self.start_astar = QtGui.QPushButton('Start Search', self)
        QtCore.QObject.connect(self.start_astar, QtCore.SIGNAL("clicked()"), self.run_astar)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.load_level_button)
        layout.addWidget(self.start_astar)

        self.init_ui()

    def init_ui(self):
        self.setGeometry(200, 200, 1024, 800)
        self.setWindowTitle('Module 1 - A* Navigation Problems')
        self.show()
        self.update()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw_board(qp)
        qp.end()

    def is_visited(self, x, y):
        y_dim = self.node.y_dim()
        return [x, y_dim - y - 1] in self.node.visited

    def is_regular(self, x, y):
        return self.board[y][x] == const.TILE

    def is_obstacle(self, x, y):
        return self.board[y][x] == const.OBSTACLE

    def is_start(self, x, y):
        return self.board[y][x] == const.START

    def is_goal(self, x, y):
        return self.board[y][x] == const.GOAL

    def draw_board(self, qp):
        if self.board is None:
            return

        for y in range(self.node.y_dim()):
            for x in range(self.node.x_dim()):
                if self.is_visited(x, y):
                    if self.is_regular(x, y):
                        qp.setBrush(QtGui.QColor(0, 220, 220))
                    elif self.is_start(x, y):
                        qp.setBrush(QtGui.QColor(0, 120, 200))
                    elif self.is_goal(x, y):
                        qp.setBrush(QtGui.QColor(0, 250, 40))
                else:
                    if self.is_regular(x, y):
                        qp.setBrush(QtGui.QColor(250, 250, 250))
                    elif self.is_obstacle(x, y):
                        qp.setBrush(QtGui.QColor(200, 0, 0))
                    elif self.is_start(x, y):
                        qp.setBrush(QtGui.QColor(0, 0, 200))
                    elif self.is_goal(x, y):
                        qp.setBrush(QtGui.QColor(0, 120, 20))

                # Draw a tile
                qp.drawRect(
                    (x * self.dx) + self.offset_x,
                    (y * self.dy) + self.offset_y,
                    self.dx, self.dy)

    def run_astar(self):
        if self.solved:
            navigation = Navigation(NavigationGrid(self.node.map, self.board), self)
        else:
            navigation = Navigation(NavigationGrid(self.node.map), self)

        self.thread.search(self, navigation)

    def paint(self, node):
        self.node  = node.state
        self.board = node.state.grid

        self.update()

    def set_tile(self, x, y, y_dim, mark):
        self.board[y_dim - y - 1][x] = mark

    def load_level(self):
        if self.board is None:
            self.filename = 'ex_simple.txt'
        else:
            path = QtGui.QFileDialog.getOpenFileName(self.window(), "Open Scenario File", "", "Text files (*.txt)")
            self.filename = list(path.split('/')).pop()

        self.node  = NavigationGrid(MapReader(self.filename))
        self.board = self.node.grid
        self.update()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Module1()
    ex.load_level()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
