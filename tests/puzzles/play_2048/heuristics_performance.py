from time import time

from src.puzzles.play_2048.play_2048_player import Play2048Player

from src.puzzles.play_2048.heuristics.random_move import RandomMove
from src.puzzles.play_2048.heuristics.snake_gradient import SnakeGradient
from src.puzzles.play_2048.heuristics.corner_gradient import CornerGradient

from src.algorithms.adversial_search.expectimax import Expectimax


def main():
    heuristics = [SnakeGradient, CornerGradient]
    plays = 5
    searches = [Expectimax]
    depths = [3, 4]

    scores = []
    for _ in range(plays):
        player = Play2048Player(RandomMove, searches[0], 1)
        player.play()
        scores.append(player.game.score)

    average = sum(scores) / float(plays)

    print 'Runs: ' + str(plays)
    print 'Random: ' + str(average) + ' average score'
    print 'Best: {}, worst: {}'.format(max(scores), min(scores))

    for search in searches:
        print 'Search: ' + search.__name__

        for heuristic in heuristics:
            for depth in depths:
                max_tiles = []
                scores = []
                timings = []

                for _ in range(plays):
                    t0 = time()
                    player = Play2048Player(heuristic, search, depth)

                    player.play()

                    timings.append(time() - t0)
                    scores.append(player.game.score)
                    max_tiles.append(2 ** player.game.max_tile())

                tot_t = sum(timings)
                average = sum(scores) / float(plays)
                avg_t = tot_t / float(plays)

                print('{} - depth {}'.format(heuristic.__name__, depth))
                print('Average score: {}'.format(average))
                print('Avg time: {:.2f} s, tot: {:.2f} s'.format(avg_t, tot_t))
                print('Best: {}, worst: {}'.format(max(scores), min(scores)))
                print('All scores: ' + str(scores))
                print('Max tiles: ' + str(max_tiles))
                print('2048s: {} of {}'.format(max_tiles.count(2048), plays))

if __name__ == '__main__':
    main()
