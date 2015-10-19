"""
Inspired by:

http://folk.ntnu.no/valerijf/NTNU/7/IT3105/Project3/Project3.pdf
https://github.com/freva/2048-AI/blob/master/src/AI/search/AlphaBeta.java
"""
from src.puzzles.play_2048.heuristics.heuristic import Heuristic


class Gradient(Heuristic):
    @classmethod
    def evaluation_function(cls, state):
        if not state.is_possible():
            return 0

        grid_component = float('-inf')

        for grid in cls.grids():
            h = 0
            for y in range(len(grid)):
                for x in range(len(grid[0])):
                    h += grid[y][x] * state.board[4 * y + x]

            grid_component = max(grid_component, h)

        free_tiles_component = state.free_tiles() / 16.0

        return grid_component * free_tiles_component

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
