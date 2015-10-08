import unittest

from src.algorithms.minimax.minimax import Minimax
from src.puzzles.play_2048.play_2048_state import Play2048State
from src.puzzles.play_2048.play_2048_player import Play2048Player

from src.puzzles.play_2048.heuristics.snake_gradient import SnakeGradient
from src.puzzles.play_2048.heuristics.log_gradient import LogGradient


class TestPlay2048Player(unittest.TestCase):
    def setUp(self):
        depth = 4
        self.minimax = Minimax(Play2048Player.actions(), depth)

    def test_minimax_correct_move(self):
        game = Play2048State(LogGradient)
        game.board = [
            [256, 128, 64, 32],
            [64, 64, 16, 8],
            [0, 0, 4, 0],
            [2, 0, 0, 0]
        ]

        suggested_move = self.minimax.alpha_beta_decision(game)
        print(suggested_move)
        print(game.evaluation_function())

    def test_minimax_run(self):

        game = Play2048State(SnakeGradient)
        game.board = [
            [4, 16, 64, 16],
            [4, 8, 0, 0],
            [0, 2, 0, 2],
            [0, 0, 0, 0]
        ]

        preferred = ['up']

        # self.preferred = ['up', 'left', 'up', 'right']

        # Up => [8, 16, 64, 16], [0, 8, 0, 2], [0, 2, 0, 0], [0, 0, 0, 0]
        # Left => [8, 16, 64, 16], [8, 2, 0, 0], [2, 0 , 0, 0], [0, 0, 0, 0]
        # Up => [16, 16, 64, 16, [2, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]
        # Right => [0, 32, 64, 16], [0, 0, 0, 4], [0, 0, 0, 0], [0, 0, 0, 0]

        for preferred in preferred:
            suggested_move = self.minimax.alpha_beta_decision(game)

            if game.move(suggested_move):
                game.next_state()

            self.assertEqual(preferred, suggested_move)

if __name__ == '__main__':
    unittest.main()
