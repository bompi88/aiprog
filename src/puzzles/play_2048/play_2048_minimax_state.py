from copy import deepcopy


class Play2048MinimaxState(object):
    def __init__(self, game):
        self.game = game

    def is_terminal(self):
        return not self.game.is_possible()

    def perform(self, action):
        game = self.game.perform_move(action)
        if game:
            return Play2048MinimaxState(game)
        else:
            return None

    def successors(self):
        successors = []
        board = self.game.board

        zero_sides = []
        sides = [0, 3]
        for x in range(4):
            for y in range(4):
                if x not in sides and y not in sides:
                    continue

                if board[y][x] is 0:
                    zero_sides.append((x, y))

        possibilities = [2, 4]

        for zero_side in zero_sides:
            for possibility in possibilities:
                new_board = deepcopy(board)

                new_board[zero_side[1]][zero_side[0]] = possibility

                new_game = self.game.copy_with_board(new_board)
                successor = Play2048MinimaxState(new_game)
                successors.append(successor)

        return successors


    def utility(self):
        board = self.game.board

        highest = max([element for row in board for element in row])

        corners = [(0, 0), (0, 3), (3, 0), (3, 3)]
        near_corners = [(0, 1), (1, 0), (0, 2), (2, 0),
                        (1, 3), (3, 1), (3, 2), (2, 3)]

        corner_bonus = False
        for y in board:
            for x in row:
                if element is highest:
                    if (x, y) in corners:
                        corner_bonus = True

        near_corner_bonus = False
        for y in board:
            for x in row:
                if element is highest:
                    if (x, y) in near_corners:
                        near_corner_bonus = True

        zeros = sum([1 for row in board for el in row if el is 0])

        return (int(zeros) * 10 +
                35 * int(near_corner_bonus) +
                80 * int(corner_bonus))
