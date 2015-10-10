import unittest

from time import time

from src.puzzles.play_2048.play_2048_player import Play2048Player

from src.puzzles.play_2048.heuristics.random_move import RandomMove
from src.puzzles.play_2048.heuristics.snake_gradient import SnakeGradient
from src.puzzles.play_2048.heuristics.corner_gradient import CornerGradient
from src.puzzles.play_2048.heuristics.ov3y import Ov3y


class TestPlay2048Player(unittest.TestCase):
    def setUp(self):
        self.heuristics = [
            SnakeGradient,
            CornerGradient,
            Ov3y
        ]
        self.plays = 3

    def test_heuristics(self):
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

        for heuristic in self.heuristics:
            depths = [1, 2, 3, 4]

            for depth in depths:
                max_tiles = []
                scores = []
                timings = []

                for _ in range(self.plays):
                    t0 = time()
                    player = Play2048Player(heuristic, depth)

                    player.play()

                    timings.append(time() - t0)
                    scores.append(player.game.score)
                    max_tiles.append(player.game.max_tile())

                tot_t = sum(timings)
                average = sum(scores) / float(self.plays)
                avg_t = tot_t / float(self.plays)

                print('{} - depth {}'.format(heuristic.__name__, depth))
                print('Average score: {}'.format(average))
                print('Avg time: {:.2f} s, tot: {:.2f} s'.format(avg_t, tot_t))
                print('Best: {}, worst: {}'.format(max(scores), min(scores)))
                print('All scores: ' + str(scores))
                print('Max tiles: ' + str(max_tiles))

if __name__ == '__main__':
    unittest.main()
