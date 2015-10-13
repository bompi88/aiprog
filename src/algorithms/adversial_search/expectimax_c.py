import ctypes
import src.c_implementations


class Expectimax(object):
    def __init__(self, actions, depth):
        path = src.c_implementations.__path__[0] + '/expectimax_lib.so'
        expectimax = ctypes.CDLL(path)

        args = (ctypes.POINTER(ctypes.c_int), ctypes.c_int)
        expectimax.decision.argtypes = args

        self.search = expectimax
        self.actions = actions.values()
        self.depth = depth

    def decision(self, board):
        board_length = len(board)
        array_type = ctypes.c_int * board_length
        result = self.search.decision(array_type(*board),
                                      ctypes.c_int(self.depth))
        return int(result)
