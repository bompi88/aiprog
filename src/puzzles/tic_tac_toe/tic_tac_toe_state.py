from copy import deepcopy
from src.algorithms.minimax.minimax import Minimax
from src.algorithms.minimax.minimax_state import MinimaxState


class TicTacToe(MinimaxState):
    def __init__(self, me, board=None):
        self.empty = 2
        self.player = 0
        self.opponent = 1

        self.me = me

        self.board = board or [self.empty] * 9

    # Search until a terminal state
    def cutoff_test(self, test):
        return sum([1 for tile in self.board if tile is self.empty]) == 0

    def perform(self, action):
        placement = action[0]
        who = action[1]

        if self.board[placement] is not self.empty:
            return None
        else:
            new_board = deepcopy(self.board)

            new_board[placement] = who
            return TicTacToe(self.me, new_board)

    def successors(self):
        successors = []
        for i, element in enumerate(self.board):
            if element is self.empty:
                new_board = deepcopy(self.board)
                new_board[i] = self.me

                successors.append(TicTacToe(self.me, new_board))

        return successors

    # Utility function
    def evaluation_function(self):
        rows, columns, diagonals = [], [], [[], []]

        for i in range(3):
            rows.append(self.board[i*3:i*3+3])

        for j in range(3):
            columns.append(self.board[j:9:3])

        for i in range(3):
            for j in range(3):
                if i == j:
                    diagonals[0].append(rows[i][j])

                if i == 2 - j:
                    diagonals[1].append(rows[i][j])

        checks = rows + columns + diagonals

        for check in checks:
            if all([True if el is self.player else False for el in check]):
                return 10
            if all([True if el is self.opponent else False for el in check]):
                return -10

        return 0

    def __str__(self):
        rows = []
        for i in range(3):
            rows.append(','.join([str(el) for el in self.board[i*3:i*3+3]]))

        return '\n'.join([row for row in rows])


def main():
    turn = 1  # Player
    state = TicTacToe(turn)

    actions = (zip(range(9), [state.player] * 9) +
               zip(range(9), [state.opponent] * 9))

    minimax = Minimax(actions, float('inf'))

    finished = False
    i = 0
    while not finished:
        move = minimax.alpha_beta_decision(state)

        if move:
            state = state.perform(move)
            turn = 1 - turn
            state.me = turn

            print('round', i)
            print state
        else:
            finished = True

        i += 1

if __name__ == '__main__':
    main()
