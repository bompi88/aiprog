import unittest

from time import time

from src.puzzles.play_2048.play_2048_player import Play2048Player

from src.puzzles.play_2048.heuristics.random_move import RandomMove
from src.puzzles.play_2048.heuristics.snake_gradient import SnakeGradient
from src.puzzles.play_2048.heuristics.top_left_gradient import TopLeftGradient


class TestPlay2048Player(unittest.TestCase):
    def setUp(self):
        self.heuristics = [
            RandomMove,
            SnakeGradient,
            TopLeftGradient
        ]
        self.plays = 5

    def test_random_play(self):
        scores = []
        for _ in range(self.plays):
            player = Play2048Player(None, RandomMove, 1)

            player.start()
            player.wait()

            scores.append(player.game.score)

        average = sum(scores) / float(self.plays)
        self.assertGreater(average, 1000)

        print('Random: ' + str(average))

    def test_snake_gradient(self):
        depths = [1, 2, 3, 4]

        for depth in depths:
            scores = []
            timings = []

            for _ in range(self.plays):
                t0 = time()
                player = Play2048Player(None, SnakeGradient, depth)

                player.start()
                player.wait()

                timings.append(time() - t0)
                scores.append(player.game.score)

            average = sum(scores) / float(self.plays)
            avg_t = sum(timings) / float(self.plays)

            print('Snake - depth {}: {}, in {} s'.format(depth, average, avg_t))

if __name__ == '__main__':
    unittest.main()

