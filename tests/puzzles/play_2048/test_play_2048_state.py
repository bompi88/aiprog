import unittest

from copy import deepcopy

from src.puzzles.play_2048.play_2048_state import Play2048State
from src.puzzles.play_2048.play_2048_player import Play2048Player


class TestPlay2048Player(unittest.TestCase):
    def setUp(self):
        self.game = Play2048State()

    def test_next_state(self):
        self.player = Play2048Player(None)
        self.game = Play2048State()

        ended = False

        moves = 0
        twos = 0
        fours = 0

        next_move = 0

        while not ended:
            did_move = self.game.move(self.player.actions().values()[next_move])

            next_move += 1
            next_move %= 4

            if not did_move:
                continue

            moves += 1

            state_sum = self.game.sum_tiles()
            state_set = self.game.set_tiles()

            tile_val = self.game.next_state()
            twos += tile_val is 2
            fours += tile_val is 4

            self.assertEqual(state_sum + tile_val, self.game.sum_tiles())
            self.assertEqual(state_set + 1, self.game.set_tiles())

            if not self.game.is_possible():
                ended = True

        twos_ratio = twos / float(moves)
        fours_ratio = fours / float(moves)
        self.assertAlmostEqual(0.9, twos_ratio, delta=0.09)
        self.assertAlmostEqual(0.1, fours_ratio, delta=0.09)

    def test_distribution_of_next_state(self):
        board = [[0, 0, 0, 0], [0, 16, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        self.game.board = deepcopy(board)

        rounds = 10000

        twos = 0
        fours = 0

        ids = [0] * 16

        for _ in range(rounds):
            tile_val = self.game.next_state()

            for x in range(4):
                for y in range(4):
                    if self.game.board[y][x] in [2, 4]:
                        tile = x + 4 * y
                        ids[tile] += 1

            self.game.board = deepcopy(board)
            twos += tile_val is 2
            fours += tile_val is 4

        ids = [element for element in ids if element is not 0]

        twos_ratio = twos / float(rounds)
        fours_ratio = fours / float(rounds)

        self.assertAlmostEqual(0.9, twos_ratio, delta=0.01)
        self.assertAlmostEqual(0.1, fours_ratio, delta=0.01)

        for i in ids:
            self.assertAlmostEqual(1 / 12.0, i / float(rounds), delta=0.01)

    def test_evaluation_function(self):
        self.game.board = [
            [256, 128, 64, 32],
            [32, 16, 32, 8],
            [2, 4, 8, 2],
            [2, 0, 0, 2]
        ]

        evaluation = (sum(self.game.board[0] * 10) +
                      sum(self.game.board[1] * 8) +
                      sum(self.game.board[2] * 4) +
                      sum(self.game.board[3]))

        # self.assertEqual(evaluation, self.game.evaluation_function())

        self.game.board[0][3] = 2
        evaluation -= 30 * 10

        evaluation /= 2

        # self.assertEqual(evaluation, self.game.evaluation_function())

if __name__ == '__main__':
    unittest.main()
