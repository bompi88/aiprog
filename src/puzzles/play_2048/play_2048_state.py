from random import randint
from copy import copy


class Play2048State(object):
    def __init__(self):
        self.board = self.start_board()

        self.possible_moves = {'left': [-1, 0], 'up': [0, -1],
                               'right': [1, 0], 'down': [0, 1]}
        self.score = 0

    @staticmethod
    def start_board():
        board = [0] * 16

        tile = randint(0, 15)
        value = 2 if randint(1, 10) is 10 else 1

        board[int(4 * (tile % 4) + tile / 4)] = value

        tile_set = tile
        while tile_set == tile:
            tile = randint(0, 15)

        value = 2 if randint(1, 10) is 10 else 1

        board[int(4 * (tile % 4) + tile / 4)] = value

        return board

    def perform(self, move):
        new_game = self.copy_with_board(copy(self.board))
        did_move = new_game.move(move)

        if did_move:
            return new_game
        else:
            return None

    def copy_with_board(self, board):
        new_state = Play2048State()
        new_state.score = self.score
        new_state.board = board

        return new_state

    def is_possible(self):
        for move in self.possible_moves.values():
            if self.slides(move, False):
                return True
            if self.collision(move, False):
                return True

        return False

    def set_tiles(self):
        return sum([0 if tile is 0 else 1 for tile in self.board])

    def sum_tiles(self):
        return sum(self.board)

    def max_tile(self):
        max_tile = float('-inf')

        for el in self.board:
            max_tile = max(max_tile, el)

        return max_tile

    def next_state(self):
        viable = []
        for x in range(4):
            for y in range(4):
                if self.board[4 * y + x] == 0:
                    viable.append((x, y))

        tile_index = randint(0, len(viable) - 1)
        tile = viable[tile_index]
        tile_value = 2 if randint(1, 10) is 10 else 1

        for x in range(4):
            for y in range(4):
                if self.board[4 * y + x] == 0:
                    if tile == (x, y):
                        self.board[4 * y + x] = tile_value

        return tile_value

    def move(self, move):
        slid = self.slides(move)
        collided = self.collision(move)

        if collided:
            self.slides(move)

        return slid or collided

    def slides(self, move, perform_move=True):
        did_move = False
        check_range = []

        if move is None:
            print(self.board)
            print(self.is_possible())

        for i in range(4):
            for j in range(4):
                x = 3 - j if move[0] == 1 else j
                y = 3 - i if move[1] == 1 else i

                tile = 4 * y + x

                if self.board[tile] is 0:
                    continue

                if move[1] is 0:  # Left or right
                    if move[0] is -1:  # Left
                        check_range = range(0, x)
                    elif move[0] is 1:  # Right
                        check_range = range(3, x, -1)

                    for x_new in check_range:
                        new_tile = 4 * y + x_new
                        if self.move_tile(tile, new_tile, perform_move):
                            did_move = True
                            break
                elif move[0] is 0:  # Up or down
                    if move[1] is -1:  # Up
                        check_range = range(0, y)
                    elif move[1] is 1:  # Down
                        check_range = range(3, y, -1)

                    for y_new in check_range:
                        new_tile = 4 * y_new + x
                        if self.move_tile(tile, new_tile, perform_move):
                            did_move = True
                            break

        return did_move

    def move_tile(self, tile, new_tile, perform_move):
        if self.board[new_tile] is not 0:
            return False

        if perform_move:
            self.board[new_tile], self.board[tile] = self.board[tile], 0

        return True

    def collision(self, move, perform_move=True):
        collision = False

        for i in range(4):
            for j in range(4):
                x = 3 - j if move[0] == 1 else j
                y = 3 - i if move[1] == 1 else i

                tile = 4 * y + x
                if self.board[tile] is 0:
                    continue

                neighbour = (x - move[0], y - move[1])
                if not (0 <= neighbour[0] < 4 and 0 <= neighbour[1] < 4):
                    continue

                neighbour_tile = 4 * neighbour[1] + neighbour[0]

                if self.board[neighbour_tile] is self.board[tile]:
                    if perform_move:
                        self.board[tile] += 1
                        self.board[neighbour_tile] = 0
                        self.score += 2 ** self.board[tile]
                    collision = True

        return collision
