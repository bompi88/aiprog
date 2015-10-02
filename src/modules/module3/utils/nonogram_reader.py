""" Represent a graph """
import os

from PyQt4 import QtGui

import res
from src.algorithms.puzzles.nonogram.nono_constraint import NonoConstraint


class NonogramReader(object):
    # pylint: disable=too-many-instance-attributes

    def __init__(self, nonogram):
        self.x, self.y, self.rows, self.columns = nonogram

        self.constraints = []
        self.variables = set([])
        self.init_constraints_and_variables()

    def init_constraints_and_variables(self):
        for i in range(self.y):
            self.variables.add('r' + str(i))

        for i in range(self.x):
            self.variables.add('c' + str(i))

        for y in range(self.y):
            for x in range(self.x):
                self.constraints.append(NonoConstraint('r{r} [{c}] == c{c} [{r}]'.format(r=y, c=x)))

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
        x, y = [int(e) for e in lines.pop(0).split(' ')]
        rows = [list(int(e) for e in lines.pop(0).split(' ')) for _ in range(y)]
        rows = list(reversed(rows))
        columns = [list(int(e) for e in lines.pop(0).split(' ')) for _ in range(x)]

        return [x, y, rows, columns]

    @staticmethod
    def read_nonogram(filename):
        """ Read a file from /maps """
        path = os.path.dirname(res.__file__)
        path += '/nonograms/' + filename
        graph_file = open(path, 'r')
        contents = graph_file.read()
        return contents.splitlines()

# NonogramReader(NonogramReader.parse_nonogram(
#     NonogramReader.read_nonogram('nono-a-easypeasy.txt')
# ))
