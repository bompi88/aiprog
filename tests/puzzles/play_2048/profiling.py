import cProfile

from src.algorithms.adversial_search.expectimax import Expectimax
from src.puzzles.play_2048.play_2048_player import Play2048Player
from src.puzzles.play_2048.heuristics.snake_gradient import SnakeGradient


def play():
    player = Play2048Player(SnakeGradient, Expectimax, 2)

    player.play()

cProfile.run('play()')
