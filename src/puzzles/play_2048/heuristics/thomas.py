# https://github.com/ThomasGjerde/AIProgrammering/blob/master/src/aiprog/twentyfortyeigth/TFEBoard.java
"""
    def evaluation_function(self):
        smoothness = 0
        max = 0
        mid_point = (0, 0)

        free = []

        max_placement = 0

        for i in range(4):
            for j in range(4):
                if self.board[j][i] == 0:
                    free.append((j, i))
                else:
                    if self.board[j][i] > max:
                        max = self.board[j][i]
                        mid_point = (j, i)

                    value = math.log(self.board[j][i]) / math.log(2.0)

                    for move in self.possible_moves.values():
                        target_value = self.find_neighbour(j, i, move)

                        if target_value != 0:
                            real_target = math.log(float(target_value)) / math.log(2.0)
                            smoothness -= abs(value - real_target)

        if max > 2048:
            max = 20
        else:
            max = math.log(max) / math.log(2.0)

        max_point = mid_point
        free_size = len(free)

        if max_point[0] in [0, 3] or max_point[1] in [0, 3]:
            max_placement = 1

            if max_point == (0, 0) or max_point == (3, 0) or max_point == (0, 3) or max_point == (3, 3):
                max_placement = 2

        return smoothness * 0.2 + max * 1 + max_placement * 0.5 + free_size * 1

    def find_neighbour(self, x, y, move):
        if move == self.possible_moves['up']:
            if y == 0:
                return 0
            else:
                for i in range(y - 1, -1, -1):
                    if self.board[i][x] != 0:
                        return self.board[i][x]
                return 0
        elif move == self.possible_moves['down']:
            if y == 3:
                return 0
            else:
                for i in range(y + 1, 4):
                    if self.board[i][x] != 0:
                        return self.board[i][x]
                return 0
        elif move == self.possible_moves['right']:
            if x == 3:
                return 0
            else:
                for i in range(x + 1, 4):
                    if self.board[y][i] != 0:
                        return self.board[y][i]
                return 0
        elif move == self.possible_moves['left']:
            if x == 0:
                return 0
            else:
                for i in range(x - 1, -1, -1):
                    if self.board[y][i] != 0:
                        return self.board[y][i]
                return 0

"""
