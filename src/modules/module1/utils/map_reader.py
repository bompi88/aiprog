""" Represent a navigable map """
import os

from PyQt4 import QtGui

import res
from src.algorithms.puzzles.navigation.utils.const import C
from src.algorithms.puzzles.navigation.navigation_grid import NavigationGrid


class MapReader(object):
    """ Helper class for reading a map from file, and parsing it into a list """
    def __init__(self, lines):
        self.dim = [int(e) for e in lines.pop(0).split(' ')]
        checkpoints = [int(e) for e in lines.pop(0).split(' ')]

        self.grid = [[C.TILE] * self.dim[1] for _ in range(self.dim[0])]

        self.start, self.goal = checkpoints[0:2], checkpoints[2:4]
        self.set(self.start, C.START)
        self.set(self.goal, C.GOAL)

        for line in lines:
            obstacle = [int(e) for e in line.split(' ')]

            x, y = obstacle[0], obstacle[1]

            for i in range(obstacle[2]):
                for j in range(obstacle[3]):
                    self.set([x + i, y + j], C.OBSTACLE)

        self.grid = tuple(tuple(t) for t in self.grid)

    def x_dim(self):
        """ Dimension in x-direction """
        return self.dim[0]

    def y_dim(self):
        """ Dimension in y-direction """
        return self.dim[1]

    def set(self, pos, mark):
        """ Set a tile in the grid """
        x = pos[0]
        y = pos[1]

        self.grid[self.y_dim() - y - 1][x] = mark

    @staticmethod
    def load_level(gui):
        """ Load level with a QFileDialog """
        if gui.node is None:
            filename = 'ex_simple.txt'
        else:
            path = QtGui.QFileDialog.getOpenFileName(
                gui.window(), "Open Map File", "", "Text files (*.txt)"
            )
            filename = list(path.split('/')).pop()

        if not filename:
            return

        lines = MapReader.read_map(filename)
        gui.level_loaded(filename, NavigationGrid(MapReader(lines)))

    @staticmethod
    def read_map(filename):
        """ Read a file from /maps """
        path = os.path.dirname(res.__file__)
        path += '/maps/' + filename
        map_file = open(path, 'r')
        contents = map_file.read()
        return contents.splitlines()
