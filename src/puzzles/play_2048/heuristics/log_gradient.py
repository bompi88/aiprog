from src.puzzles.play_2048.heuristics.heuristic import Heuristic

from math import log


class LogGradient(Heuristic):
    @classmethod
    def evaluation_function(cls, state):
        grid = [
            [10, 9, 8, 7],
            [9, 6, 5, 4],
            [8, 5, 3, 2],
            [7, 4, 2, 1]
        ]

        h = 0
        for y, row in enumerate(state.board):
            for x, element in enumerate(row):
                if element > 0:
                    h += grid[y][x] * log(element, 2)

        return h
