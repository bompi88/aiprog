import ctypes
import src.c_implementations


class Expectimax(object):
    def __init__(self, depth):
        path = src.c_implementations.__path__[0] + '/expectimax_lib.so'
        _expectimax = ctypes.CDLL(path)

        args = (ctypes.POINTER(ctypes.c_int), ctypes.c_int)
        _expectimax.expectimax_decision.argtypes = args

        self.expectimax = _expectimax
        self.depth = depth

    def expectimax_decision(self, board):
        board_length = len(board)
        array_type = ctypes.c_int * board_length
        result = self.expectimax.expectimax_decision(array_type(*board),
                                                     ctypes.c_int(self.depth))
        return int(result)
