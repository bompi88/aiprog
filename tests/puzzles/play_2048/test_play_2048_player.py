import unittest

from src.puzzles.play_2048.play_2048_state import Play2048State
from src.puzzles.play_2048.play_2048_player import Play2048Player


class TestPlay2048Player(unittest.TestCase):
    def setUp(self):
        self.game = Play2048State()
        self.player = Play2048Player(None)
        self.player.game = self.game

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
        # self.assertEqual(4, self.player.score)
        self.assertEqual(self.game.board,
                         [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [2, 4, 0, 0],
                          [4, 4, 2, 0]])

        self.game.move('left')
        # self.assertEqual(12, self.player.score)


if __name__ == '__main__':
    unittest.main()
