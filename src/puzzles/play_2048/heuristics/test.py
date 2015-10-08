"""
    def evaluation_function(self):
        if not self.is_possible():
            return -1000

        evaluation = 0

        row_multis = [100, 20, 4, 1]

        penalty = False
        last_row_sum = float('inf')

        for i, row in enumerate(self.board):
            row_value = sum(row) * row_multis[i]

            if last_row_sum < sum(row):
                penalty = True
            last_row_sum = sum(row)

            if max(row) > 16:
                row_value *= math.log(max(row) / 4, 2)

            monotonicity_bonus = 0
            if sorted(row) == row or list(reversed(sorted(row))) == row:
                monotonicity_bonus = 3

            evaluation += row_value * monotonicity_bonus

        if max(self.board[1]) > max(self.board[0]):
            evaluation /= 10.0

        if max(self.board[2]) >= max(self.board[1]) >= max(self.board[0]):
            evaluation /= 50.0

        if penalty:
            evaluation /= 100.0

        # Penalize 16 and below in top column in late stages
        # if max(self.board[0]) > 128:
        #     if min(self.board[0]) < 32:
        #         evaluation /= 2

        return evaluation
"""