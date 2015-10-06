from random import randint


class Play2048(object):
    def __init__(self):
        self.board = [[0] * 4 for _ in range(4)]

        tile = randint(0, 15)
        type = 4 if randint(1, 10) is 10 else 2

        self.board[tile % 4][tile / 4] = type

    def next_state(self):
        viable = 0
        sides = [0, 3]
        for x in range(4):
            for y in range(4):
                if x not in sides and y not in sides:
                    continue

                if self.board[y][x] == 0:
                    viable += 1

        tile = randint(0, viable)

        i = 0

        for x in range(4):
            for y in range(4):
                if x not in sides and y not in sides:
                    continue

                if self.board[y][x] == 0:
                    if i == tile:
                        self.board[y][x] = 4 if randint(1, 10) is 10 else 2
                    i += 1
