""" Represent a graph """
import os
import res
from PyQt4 import QtGui


class NonogramReader(object):
    # pylint: disable=too-many-instance-attributes

    def __init__(self, nonogram):
        self.x, self.y, self.rows, self.columns = nonogram

        print(list(reversed(self.rows)))
        print(self.columns)

        self.solution = [
            [0, 0, 1, 1, 1, 1, 0, 0, 0, 0], # 4
            [0, 1, 1, 1, 1, 1, 1, 0, 0, 0], # 6
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0], # 8
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0], # 8
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1], # 8
            [], # 8
            [], # 8
            [], # 8
            [], # 6
            []  # 4
        ]

        for i in range(5):
            self.solution[9 - i] = self.solution[i]

        print(self.solution)

        self.constraints = []
        self.variables = set([])
        self.init_constraints_and_variables()

    def init_constraints_and_variables(self):
        pass

    @staticmethod
    def load_level(gui):
        """ Load level with a QFileDialog """
        if gui.nonogram is None:
            filename = 'nono-heart-1.txt'
        else:
            path = QtGui.QFileDialog.getOpenFileName(
                gui.window(), "Open Map File", "", "Text files (*.txt)"
            )
            filename = list(path.split('/')).pop()

        if not filename:
            return

        return [
            filename,
            NonogramReader(
                NonogramReader.parse_nonogram(
                    NonogramReader.read_nonogram(filename)
                )
            )
        ]

    @staticmethod
    def parse_nonogram(lines):
        x, y = [int(e) for e in lines[0].split(' ')]
        rows = [list(int(e) for e in lines.pop().split(' ')) for _ in range(y)]
        columns = [list(int(e) for e in lines.pop().split(' ')) for _ in range(x)]

        return [x, y, rows, columns]

    @staticmethod
    def read_nonogram(filename):
        """ Read a file from /maps """
        path = os.path.dirname(res.__file__)
        path += '/nonograms/' + filename
        graph_file = open(path, 'r')
        contents = graph_file.read()
        return contents.splitlines()

NonogramReader(NonogramReader.parse_nonogram(
    NonogramReader.read_nonogram('nono-heart-1.txt')
))
