from random import randint
from copy import deepcopy

from src.algorithms.minimax.minimax_state import MinimaxState


class Play2048State(MinimaxState):
    def __init__(self, heuristic):
        self.board = self.start_board()
        self.successors = None

        self.possible_moves = {'left': [-1, 0], 'up': [0, -1],
                               'right': [1, 0], 'down': [0, 1]}
        self.score = 0
        self.heuristic = heuristic

    @staticmethod
    def start_board():
        board = [[0] * 4 for _ in range(4)]

        tile = randint(0, 15)
        value = 4 if randint(1, 10) is 10 else 2

        board[tile % 4][tile / 4] = value

        return board

    def perform(self, move):
        new_game = self.copy_with_board(deepcopy(self.board))
        did_move = new_game.move(move)

        if did_move:
            return new_game
        else:
            return None

    def copy_with_board(self, board):
        new_state = Play2048State(self.heuristic)
        new_state.score = self.score
        new_state.board = board

        return new_state

    def is_possible(self):
        board = self.board
        possible = False
        for move in self.possible_moves.values():
            if self.slides(move, board, False):
                possible = True
                break
            if self.collision(move, board, False):
                possible = True
                break

        return possible

    def free_tiles(self):
        return 16 - self.set_tiles()

    def set_tiles(self):
        return sum([0 if tile is 0 else 1 for r in self.board for tile in r])

    def sum_tiles(self):
        return sum([tile for row in self.board for tile in row])

    def max_tile(self):
        max_tile = float('-inf')

        for row in self.board:
            max_tile = max(max_tile, max(row))

        return max_tile

    def cutoff_test(self, depth):
        # With our heuristics, the start is not important
        return depth is 0 or self.max_tile() < 32

    def generate_successors(self, is_max):
        self.successors = []

        if is_max:
            self.successor_moves()
        else:
            self.successor_spawns()

        return self.successors

    def successor_moves(self):
        for move in self.possible_moves:
            successor = self.copy_with_board(deepcopy(self.board))

            if successor.move(move):
                self.successors.append(successor)

    def successor_spawns(self):
        zero_tiles = []
        for x in range(4):
            for y in range(4):
                if self.board[y][x] is 0:
                    zero_tiles.append((x, y))

        possibilities = [2, 4]

        for tile in zero_tiles:
            for possibility in possibilities:
                new_board = deepcopy(self.board)
                new_board[tile[1]][tile[0]] = possibility

                successor = self.copy_with_board(new_board)
                self.successors.append(successor)

    def evaluation_function(self):
        return self.heuristic.evaluation_function(self)

    def next_state(self):
        viable = []
        for x in range(4):
            for y in range(4):
                if self.board[y][x] == 0:
                    viable.append((x, y))

        tile_index = randint(0, len(viable) - 1)
        tile = viable[tile_index]
        tile_value = 4 if randint(1, 10) is 10 else 2

        for x in range(4):
            for y in range(4):
                if self.board[y][x] == 0:
                    if tile == (x, y):
                        self.board[y][x] = tile_value

        return tile_value

    def move(self, move=None):
        if not move:
            move = self.possible_moves.values()[randint(0, 3)]

        if isinstance(move, str):
            move = move.lower()
            if move not in self.possible_moves.keys():
                raise Exception('Invalid move')

            move = self.possible_moves[move]

        board = self.board
        did_slides = self.slides(move, board)
        collision = self.collision(move, board)

        did_slides_after_collision = False
        if collision:
            did_slides_after_collision = self.slides(move, board)

        did_move = did_slides or collision or did_slides_after_collision
        return did_move

    def slides(self, move, board, perform_move=True):
        did_move = False

        for i in range(4):
            for j in range(4):
                x = 3 - j if move[0] == 1 else j
                y = 3 - i if move[1] == 1 else i

                if board[y][x] is 0:
                    continue

                move_to = (x + move[0], y + move[1])

                if move == self.possible_moves['right']:
                    for x_new in range(3, move_to[0] - 1, -1):
                        if x_new in range(4) and move_to[1] in range(4):
                            if board[move_to[1]][x_new] == 0:
                                if perform_move:
                                    board[move_to[1]][x_new] = board[y][x]
                                    board[y][x] = 0
                                did_move = True
                                break
                elif move == self.possible_moves['left']:
                    check_range = range(0, move_to[0] + 1)
                    for x_new in check_range:
                        if x_new in range(4) and move_to[1] in range(4):
                            if board[move_to[1]][x_new] == 0:
                                if perform_move:
                                    board[move_to[1]][x_new] = board[y][x]
                                    board[y][x] = 0
                                did_move = True
                                if did_move:
                                    break
                elif move == self.possible_moves['down']:
                    check_range = range(3, move_to[1] - 1, -1)
                    for y_new in check_range:
                        if move_to[0] in range(4) and y_new in range(4):
                            if board[y_new][move_to[0]] == 0:
                                if perform_move:
                                    board[y_new][move_to[0]] = board[y][x]
                                    board[y][x] = 0
                                did_move = True
                                break
                elif move == self.possible_moves['up']:
                    check_range = range(0, move_to[1] + 1)
                    for y_new in check_range:
                        if move_to[0] in range(4) and y_new in range(4):
                            if board[y_new][move_to[0]] == 0:
                                if perform_move:
                                    board[y_new][move_to[0]] = board[y][x]
                                    board[y][x] = 0
                                did_move = True
                                break
        return did_move

    def collision(self, move, board, perform_move=True):
        collision = False

        for i in range(4):
            for j in range(4):
                if move[0] == 1:
                    x = 3 - j
                else:
                    x = j

                if move[1] == 1:
                    y = 3 - i
                else:
                    y = i

                neighbour = (x - move[0], y - move[1])
                if neighbour[0] in range(4) and neighbour[1] in range(4):
                    if board[y][x] is 0:
                        continue
                    if board[neighbour[1]][neighbour[0]] == board[y][x]:
                        if perform_move:
                            board[y][x] *= 2
                            board[neighbour[1]][neighbour[0]] = 0
                            self.score += board[y][x]
                        collision = True

        return collision
