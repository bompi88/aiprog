""" Represent a navigable map """
from src.utils.const import C


class Map(object):
    """ Helper class for reading a map from file, and parsing it into a list """
    def __init__(self, lines):
        self.dim = [int(e) for e in lines.pop(0).split(' ')]
        checkpoints = [int(e) for e in lines.pop(0).split(' ')]

        self.grid = [[C.nav_tile.TILE]*self.dim[1] for _ in range(self.dim[0])]

        self.start, self.goal = checkpoints[0:2], checkpoints[2:4]
        self.set(self.start, C.nav_tile.START)
        self.set(self.goal, C.nav_tile.GOAL)

        for line in lines:
            obstacle = [int(e) for e in line.split(' ')]

            x, y = obstacle[0], obstacle[1]

            for i in range(obstacle[2]):
                for j in range(obstacle[3]):
                    self.set([x + i, y + j], C.nav_tile.OBSTACLE)

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
