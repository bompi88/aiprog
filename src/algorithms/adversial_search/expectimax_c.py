import ctypes
import src.c_implementations


class ExpectimaxC(object):
    def __init__(self, actions, depth):
        path = src.c_implementations.__path__[0] + '/expectimax_lib.so'
        expectimax = ctypes.CDLL(path)

        args = (ctypes.POINTER(ctypes.c_int), ctypes.c_int)
        expectimax.decision.argtypes = args
        expectimax.decision.restype = ctypes.c_int

        self.search = expectimax
        self.actions = actions
        self.depth = depth

    def decision(self, board):
        cur_board = board.board
        board_length = len(cur_board)
        result = self.search.decision((ctypes.c_int * board_length)(*cur_board),
                                      ctypes.c_int(self.depth))
        mapping = ['left', 'up', 'right', 'down']
        move = board.possible_moves[mapping[result]]
        return move
