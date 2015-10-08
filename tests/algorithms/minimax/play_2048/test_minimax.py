import unittest

from src.algorithms.minimax.minimax import Minimax
from src.puzzles.play_2048.play_2048_state import Play2048State


class TestPlay2048Player(unittest.TestCase):
    def setUp(self):
        actions = {'left': [-1, 0], 'up': [0, -1],
                   'right': [1, 0], 'down': [0, 1]}
        depth = 3
        self.minimax = Minimax(actions, depth)
        self.game = Play2048State()
        self.game.board = [
            [4, 16, 64, 16],
            [4, 8, 0, 0],
            [0, 2, 0, 2],
            [0, 0, 0, 0]
        ]

        self.preferred = ['left', 'up', 'left', 'right']

        # TODO self.preferred = ['up', 'left', 'up', 'right']

        # Up => [8, 16, 64, 16], [0, 8, 0, 2], [0, 2, 0, 0], [0, 0, 0, 0]
        # Left => [8, 16, 64, 16], [8, 2, 0, 0], [2, 0 , 0, 0], [0, 0, 0, 0]
        # Up => [16, 16, 64, 16, [2, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]
        # Right => [0, 32, 64, 16], [0, 0, 0, 4], [0, 0, 0, 0], [0, 0, 0, 0]

    def test_minimax_run(self):
        # still_possible = True
        # while still_possible:
        for preferred in self.preferred:
            print('round')
            suggested_move = self.minimax.alpha_beta_decision(self.game)

            if self.game.move(suggested_move):
                self.game.next_state()

            print 'round finished ' + str(self.game.evaluation_function())
            # print self.game.evaluation_function()

            # self.assertEqual(preferred, suggested_move)

        #    still_possible = self.game.is_possible()

        print self.game.board
        print self.game.evaluation_function()

if __name__ == '__main__':
    unittest.main()
