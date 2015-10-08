from random import randint
from src.puzzles.play_2048.heuristics.heuristic import Heuristic


class RandomMove(Heuristic):
    @classmethod
    def evaluation_function(cls, board):
        return randint(0, 10)
