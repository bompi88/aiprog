import unittest

from copy import deepcopy

from src.puzzles.play_2048.play_2048_state import Play2048State
from src.puzzles.play_2048.play_2048_player import Play2048Player

from src.puzzles.play_2048.heuristics.snake_gradient import SnakeGradient


class TestPlay2048Player(unittest.TestCase):
    def setUp(self):
        self.game = Play2048State(SnakeGradient)
        self.moves = Play2048Player.actions().values()

    def test_next_state(self):
        ended = False

        moves = 0
        twos = 0
        fours = 0

        next_move = 0

        while not ended:
            did_move = self.game.move(self.moves[next_move])

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
        board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

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

        twos_ratio = twos / float(rounds)
        fours_ratio = fours / float(rounds)

        self.assertAlmostEqual(0.9, twos_ratio, delta=0.01)
        self.assertAlmostEqual(0.1, fours_ratio, delta=0.01)

        for i in ids:
            self.assertAlmostEqual(1 / 16.0, i / float(rounds), delta=0.01)

    def test_move_slide(self):
        self.game.board = [[2, 4, 0, 0],
                           [0, 0, 8, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0]]

        self.game.move([1, 0])

        self.assertEqual(self.game.board,
                         [[0, 0, 2, 4],
                          [0, 0, 0, 8],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]])

        self.game.move([0, 1])

        self.assertEqual(self.game.board,
                         [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 4],
                          [0, 0, 2, 8]])

        self.game.move([-1, 0])

        self.assertEqual(self.game.board,
                         [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [4, 0, 0, 0],
                          [2, 8, 0, 0]])

        self.game.move([0, -1])

        self.assertEqual(self.game.board,
                         [[4, 8, 0, 0],
                          [2, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]])

    def test_move_collision(self):
        self.game.board = [[4, 4, 0, 0],
                           [0, 16, 8, 0],
                           [0, 0, 0, 0],
                           [0, 8, 8, 16]]

        self.game.move([1, 0])

        self.assertEqual(self.game.board,
                         [[0, 0, 0, 8],
                          [0, 0, 16, 8],
                          [0, 0, 0, 0],
                          [0, 0, 16, 16]])

        self.game.move([0, 1])

        self.assertEqual(self.game.board,
                         [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 16],
                          [0, 0, 32, 16]])

        self.game.move([0, 1])

        self.assertEqual(self.game.board,
                         [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 32, 32]])

        self.game.move([1, 0])

        self.assertEqual(self.game.board,
                         [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 64]])

    def test_long_collision(self):
        self.game.board = [[0, 0, 2, 0],
                           [0, 0, 2, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0]]

        self.game.move([0, 1])

        self.assertEqual(self.game.board,
                         [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 4, 0]])

    def test_exercise_example(self):
        self.game.board = [[32, 16, 8, 0],
                           [16, 4, 4, 4],
                           [2, 2, 2, 2],
                           [0, 0, 0, 0]]

        self.game.move([1, 0])

        self.assertEqual(self.game.board,
                         [[0, 32, 16, 8],
                          [0, 16, 4, 8],
                          [0, 0, 4, 4],
                          [0, 0, 0, 0]])

    def test_left_slide(self):
        self.game.board = [[0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 2, 8],
                           [16, 32, 64, 2]]

        self.game.move([-1, 0])

        self.assertEqual(self.game.board,
                         [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [2, 8, 0, 0],
                          [16, 32, 64, 2]])

    def test_up_slide(self):
        self.game.board = [[0, 0, 0, 16],
                           [0, 0, 0, 8],
                           [0, 0, 2, 4],
                           [0, 0, 4, 2]]

        self.game.move('up')

        self.assertEqual(self.game.board,
                         [[0, 0, 2, 16],
                          [0, 0, 4, 8],
                          [0, 0, 0, 4],
                          [0, 0, 0, 2]])

    def test_end_states(self):
        self.game.board = [[8, 2, 4, 8],
                           [4, 8, 2, 4],
                           [2, 4, 8, 16],
                           [8, 2, 4, 8]]

        self.assertFalse(self.game.is_possible())

        self.assertEqual(self.game.board,
                         [[8, 2, 4, 8],
                          [4, 8, 2, 4],
                          [2, 4, 8, 16],
                          [8, 2, 4, 8]])

    def test_score(self):
        self.game.board = [[0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [2, 0, 0, 4],
                           [4, 2, 2, 2]]

        self.game.move('left')
        self.assertEqual(4, self.game.score)

        self.assertEqual(self.game.board,
                         [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [2, 4, 0, 0],
                          [4, 4, 2, 0]])

        self.game.move('left')
        self.assertEqual(12, self.game.score)

if __name__ == '__main__':
    unittest.main()
