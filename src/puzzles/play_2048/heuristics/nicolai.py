# Evaluation function
# https://github.com/Nicola17/term2048-AI/blob/34903b680c1dd87536a828db0849ab51f441376c/term2048-AI/ia.py
"""
    def evaluation_function(self):
        commonRatio=0.25
        linearWeightedVal = 0
        invert = False
        weight = 4000000.
        minimum_value = self.board[0][0]
        malus = 0
        for y in range(4):
            for x in range(4):
                b_x = x
                if invert:
                    b_x = 4 - 1 - x

                current_value=self.board[y][b_x]
                linearWeightedVal += current_value*weight
                weight *= commonRatio

                if current_value < minimum_value:
                    minimum_value = current_value
                else:
                    malus += current_value - minimum_value

            invert = not invert

        return max(linearWeightedVal-malus,0)
"""
