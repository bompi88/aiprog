import unittest

from src.algorithms.adversial_search.expectimax import Expectimax
from src.puzzles.play_2048.play_2048_state import Play2048State
from src.puzzles.play_2048.play_2048_player import Play2048Player

from src.puzzles.play_2048.heuristics.corner_gradient import CornerGradient


class TestPlay2048Player(unittest.TestCase):
    def setUp(self):
        depth = 3
        self.actions = Play2048Player.actions()
        self.moves = {','.join(map(str, v)): k for k, v in self.actions.items()}
        self.search = Expectimax(self.actions.values(), depth)

    def test_minimax_correct_move(self):
        game = Play2048State(CornerGradient)
        game.board = [
            256, 128, 64, 32,
            64, 64, 16, 8,
            0, 0, 4, 0,
            2, 0, 0, 0
        ]

        suggested_move = self.search.decision(game)
        self.assertEqual('down', self.moves[','.join(map(str, suggested_move))])

    def test_minimax_run(self):
        game = Play2048State(CornerGradient)
        game.board = [
            4, 16, 64, 16,
            4, 8, 0, 0,
            0, 2, 0, 2,
            0, 0, 0, 0
        ]

        preferred = ['left', 'up', 'down', 'right']

        suggested = []

        for _ in preferred:
            suggested_move = self.search.decision(game)
            suggested.append(self.moves[','.join(map(str, suggested_move))])

            game.move(suggested_move)
            # game.next_state() - Skip new tile, to keep result deterministic.

        self.assertEqual(preferred, suggested)

if __name__ == '__main__':
    unittest.main()
