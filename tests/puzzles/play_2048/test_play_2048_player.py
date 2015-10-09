import unittest

from time import time

from src.puzzles.play_2048.play_2048_player import Play2048Player

from src.puzzles.play_2048.heuristics.random_move import RandomMove
from src.puzzles.play_2048.heuristics.snake_gradient import SnakeGradient
from src.puzzles.play_2048.heuristics.top_left_gradient import TopLeftGradient
from src.puzzles.play_2048.heuristics.ov3y import Ov3y


class TestPlay2048Player(unittest.TestCase):
    def setUp(self):
        self.heuristics = [
            SnakeGradient,
            TopLeftGradient,
            Ov3y
        ]
        self.plays = 5

    def test_random_play(self):
        scores = []
        for _ in range(self.plays):
            player = Play2048Player(RandomMove, 1)

            player.play()

            scores.append(player.game.score)

        average = sum(scores) / float(self.plays)
        self.assertGreater(average, 1000)

        print('Runs: ' + str(self.plays))
        print('Random: ' + str(average) + ' average score')
        print('Best: {}, worst: {}'.format(max(scores), min(scores)))

    def test_heuristics(self):
        for heuristic in self.heuristics:
            depths = [1, 2, 3, 4]

            for depth in depths:
                scores = []
                timings = []

                for _ in range(self.plays):
                    t0 = time()
                    player = Play2048Player(heuristic, depth)

                    player.play()

                    timings.append(time() - t0)
                    scores.append(player.game.score)

                tot_t = sum(timings)
                average = sum(scores) / float(self.plays)
                avg_t = tot_t / float(self.plays)

                print('{} - depth {}: {} average score'.format(heuristic.__name__ , depth, average))
                print('Average time: {:.2f}, total: {:.2f}'.format(avg_t, tot_t))
                print('Best: {}, worst: {}'.format(max(scores), min(scores)))

if __name__ == '__main__':
    unittest.main()
