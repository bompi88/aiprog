import unittest

from src.puzzles.play_2048.play_2048 import Play2048
from src.puzzles.play_2048.play_2048_player import Play2048Player


class TestPlay2048Player(unittest.TestCase):
    def setUp(self):
        self.game = Play2048()
        self.player = Play2048Player(None)
        self.player.game = self.game

    def test_move_slide(self):
        self.game.board = [[2, 4, 0, 0],
                           [0, 0, 8, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0]]

        self.player.move([1, 0])

        self.assertEqual(self.game.board,
                         [[0, 0, 2, 4],
                          [0, 0, 0, 8],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]])

        self.player.move([0, 1])


        self.assertEqual(self.game.board,
                         [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 4],
                          [0, 0, 2, 8]])

        self.player.move([-1, 0])

        self.assertEqual(self.game.board,
                         [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [4, 0, 0, 0],
                          [2, 8, 0, 0]])

        self.player.move([0, -1])

        self.assertEqual(self.game.board,
                         [[4, 8, 0, 0],
                          [2, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]])

    def test_move_collision(self):
        self.game.board = [[4, 4, 0, 0],
                           [0, 16, 8, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0]]

        self.player.move([1, 0])

        self.assertEqual(self.game.board,
                         [[0, 0, 0, 8],
                          [0, 0, 16, 8],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]])

        self.player.move([0, 1])

        self.assertEqual(self.game.board,
                         [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 16, 16]])

        self.player.move([1, 0])

        self.assertEqual(self.game.board,
                         [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 32]])


if __name__ == '__main__':
    unittest.main()
