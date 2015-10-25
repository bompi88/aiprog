import ctypes
import src.c_implementations


class ExpectimaxC(object):
    def __init__(self, _, depth):
        self.path = src.c_implementations.__path__[0] + '/expectimax_lib.so'
        self.search = ctypes.CDLL(self.path)

        self.depth = depth

    def decision(self, board):
        b = board.board
        d = self.depth
        result = self.search.decision(d, b[0], b[1], b[2], b[3], b[4], b[5],
                                         b[6], b[7], b[8], b[9], b[10],
                                         b[11], b[12], b[13], b[14], b[15])
        print(result)

        index = (result * 2) / 2

        mapping = ['left', 'up', 'right', 'down']
        move = board.possible_moves[mapping[index]]
        return move
