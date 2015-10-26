from time import time

from src.puzzles.play_2048.play_2048_player import Play2048Player
from src.algorithms.adversial_search.expectimax_c import ExpectimaxC


def main():
    plays = 10

    constants = [
        ('smoothness', 0.23),
        ('max_tile', 1.0),
        ('free_tiles', 2.3),
        ('max_placement', 1.0),
        ('monotonicity', 1.9)
    ]
    multipliers = [0.75, 0.9, 1, 1.10, 1.25]

    search = ExpectimaxC
    depth = 2

    print 'Search: ' + search.__name__ + '\n'

    for constant in constants:
        print('Playing with: ' + str(constant[0]).capitalize())
        print('')

        for multiplier in multipliers:
            max_tiles = []
            scores = []
            timings = []

            player = None

            for _ in range(plays):
                player = Play2048Player(None, search, depth)
                t0 = time()

                sm = multiplier if constant[0] == 'smoothness' else 1
                mm = multiplier if constant[0] == 'max_tile' else 1
                fm = multiplier if constant[0] == 'free_tiles' else 1
                mpm = multiplier if constant[0] == 'max_placement' else 1
                mom = multiplier if constant[0] == 'monotonicity' else 1

                player.search.smoothness_constant = constants[0][1] * sm
                player.search.max_tile_constant = constants[1][1] * mm
                player.search.free_tiles_constant = constants[2][1] * fm
                player.search.max_placement_constant = constants[3][1] * mpm
                player.search.monotonicity_constant = constants[4][1] * mom

                player.play()

                timings.append(time() - t0)
                scores.append(player.game.score)
                max_tiles.append(2 ** player.game.max_tile())

            tot_t = sum(timings)
            average = sum(scores) / float(plays)
            avg_t = tot_t / float(plays)

            print('Smoothness: {}, Max tile: {}, Free tiles: {}'.format(
                player.search.smoothness_constant,
                player.search.max_tile_constant,
                player.search.free_tiles_constant
            ))
            print('Max placement: {}, Monotonicity: {}'.format(
                player.search.max_placement_constant,
                player.search.monotonicity_constant
            ))
            print('Average score: {}'.format(average))
            print('Avg time: {:.2f} s, tot: {:.2f} s'.format(avg_t, tot_t))
            print('Best: {}, worst: {}'.format(max(scores), min(scores)))
            print('All scores: ' + str(scores))
            print('Max tiles: ' + str(max_tiles))
            print('2048s: {} of {}'.format(max_tiles.count(2048), plays))
            print('')

if __name__ == '__main__':
    main()
