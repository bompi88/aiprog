from src.puzzles.play_2048.heuristics.gradient import Gradient


class SnakeGradient(Gradient):
    @classmethod
    def mask(cls):
        return [
            [16, 15, 14, 13],
            [9, 10, 11, 12],
            [8, 7, 6, 5],
            [1, 2, 3, 4]
        ]