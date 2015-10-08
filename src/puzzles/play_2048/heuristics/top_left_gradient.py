from src.puzzles.play_2048.heuristics.gradient import Gradient


class SnakeGradient(Gradient):
    @classmethod
    def mask(cls):
        return [
            [10, 9, 8, 7],
            [9, 6, 5, 4],
            [8, 5, 3, 2],
            [7, 4, 2, 1]
        ]
