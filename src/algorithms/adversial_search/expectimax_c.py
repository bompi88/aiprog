import ctypes
import src.clibs


class ExpectimaxC(object):
    def __init__(self, _, depth):
        self.path = src.clibs.__path__[0] + '/expectimax_lib.so'
        self.search = ctypes.CDLL(self.path)

        self.depth = depth

        self.smoothness_constant = 0.23
        self.max_tile_constant = 1.0
        self.free_tiles_constant = 2.3
        self.max_placement_constant = 1.0
        self.monotonicity_constant = 1.9

    def decision(self, board):
        b = board.board
        result = self.search.decision(
            self.depth, b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[8],
                        b[9], b[10], b[11], b[12], b[13], b[14], b[15],
            ctypes.c_double(self.smoothness_constant),
            ctypes.c_double(self.max_tile_constant),
            ctypes.c_double(self.free_tiles_constant),
            ctypes.c_double(self.max_placement_constant),
            ctypes.c_double(self.monotonicity_constant)
        )

        mapping = ['left', 'up', 'right', 'down']
        move = board.possible_moves[mapping[result]]
        return move
