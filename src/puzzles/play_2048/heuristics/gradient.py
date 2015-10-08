"""
Inspired by:

http://folk.ntnu.no/valerijf/NTNU/7/IT3105/Project3/Project3.pdf
https://github.com/freva/2048-AI/blob/master/src/AI/search/AlphaBeta.java
"""


class Gradient(object):
    @classmethod
    def evaluation_function(cls, board):
        max_h = float('-inf')

        for grid in cls.grids():
            h = 0
            for x, row in enumerate(board):
                for y, element in enumerate(row):
                    h += grid[y][x] * element

            max_h = max(max_h, h)

        return max_h

    @classmethod
    def grids(cls):
        grids = []

        grid = cls.mask()
        grids.append(grid)

        for i in range(3):
            grid = zip(*grid[::-1])
            grids.append(grid)

        return grids

    @classmethod
    def mask(cls):
        raise NotImplementedError('Implement mask in Gradient() subclass')
