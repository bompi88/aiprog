import sys
from PyQt4 import QtGui, QtCore

# Has to install tkinter:
# pip install tkinter


class Module1(QtGui.QWidget):

    def __init__(self):
        super(Module1, self).__init__()

        self.board = None
        self.dx = 20  # Pixels per tile in x-direction
        self.dy = 20  # Pixels per tile in y-direction
        self.offset_x = 50  # Offset from left
        self.offset_y = 50  # Offset from top

        self.button = QtGui.QPushButton('Load new level', self)
        QtCore.QObject.connect(self.button, QtCore.SIGNAL("clicked()"), self.load_level)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.button)

        self.init_ui()

    def init_ui(self):

        self.setGeometry(200, 200, 1024, 800)
        self.setWindowTitle('Module 1 - A* Navigation Problems')
        self.show()

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw_board(qp)
        qp.end()

    def draw_board(self, qp):

        if self.board is None:
            return

        for x in range(len(self.board)):
            for y in range(len(self.board[0])):
                if self.board[x][y] is 0:
                    qp.setBrush(QtGui.QColor(250, 250, 250))  # Regular tile
                elif self.board[x][y] is 1:
                    qp.setBrush(QtGui.QColor(200, 0, 0))  # Obstacles
                elif self.board[x][y] is 2:
                    qp.setBrush(QtGui.QColor(0, 0, 200))  # Start node
                elif self.board[x][y] is 3:
                    qp.setBrush(QtGui.QColor(0, 200, 0))  # End node

                # Draw a tile
                qp.drawRect((x * self.dx) + self.offset_x,
                            ((len(self.board[0]) - y - 1) * self.dy) + self.offset_y,
                            self.dx,
                            self.dy)

    def load_level(self):
        lines = self.read_file()

        # Create the matrix
        dim = [int(n) for n in lines.pop(0).split()]
        self.board = [[0 for x in range(dim[0])] for x in range(dim[1])]

        # Set start and end points
        endpoints = [int(n) for n in lines.pop(0).split()]
        self.board[endpoints[0]][endpoints[1]] = 2
        self.board[endpoints[2]][endpoints[3]] = 3

        for line in lines:
            obstacle = [int(n) for n in line.split()]

            x = obstacle[0]
            y = obstacle[1]

            for lx in range(obstacle[2]):
                for ly in range(obstacle[3]):
                    self.board[x + lx][y + ly] = 1

        print self.board

    def read_file(self):

        if self.board is None:
            path = 'ex_simple.txt'
        else:
            path = QtGui.QFileDialog.getOpenFileName(self.window(), "Open Scenario File", "", "Text files (*.txt)")

        with open(path) as f:
            return f.readlines()


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Module1()
    ex.load_level()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
