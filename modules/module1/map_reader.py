import os

import modules
from algorithms.astar.navigation.const import *


class MapReader:
    def __init__(self, filename):
        self.lines = self.read_file(filename)

        self.dim    = map(int, self.lines.pop(0).split(' '))
        checkpoints = map(int, self.lines.pop(0).split(' '))

        self.grid = [[const.TILE] * self.dim[1] for i in range(self.dim[0])]

        start, goal = checkpoints[0:2], checkpoints[2:4]
        self.set(start, const.START)
        self.set(goal, const.GOAL)

        self.start = tuple(start)
        self.goal  = tuple(goal)

        self.visited = []
        self.visited.append(start)
        self.current_pos = start

        while self.lines:
            line     = self.lines.pop(0)
            obstacle = map(int, line.split(' '))

            x, y = obstacle[0], obstacle[1]

            for i in range(obstacle[2]):
                for j in range(obstacle[3]):
                    self.set([x + i, y + j], const.OBSTACLE)

    def x_dim(self):
        return self.dim[0]

    def y_dim(self):
        return self.dim[1]

    def set(self, pos, mark):
        x = pos[0]
        y = pos[1]

        self.grid[self.y_dim() - y - 1][x] = mark

    def read_file(self, filename):
        path = os.path.dirname(modules.__file__)
        path += '/module1/maps/' + filename
        file        = open(path, 'r')
        contents    = file.read()
        return contents.splitlines()
