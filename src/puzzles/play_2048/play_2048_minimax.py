class Play2048Minimax(object):
    def __init__(self):
        self.actions = {'left': [-1, 0], 'up': [0, -1],
                        'right': [1, 0], 'down': [0, 1]}

        self.depth = 6

    def minimax_decision(self, state):
        max_value = float('-inf')
        max_a = None

        for a in self.actions:
            result = state.perform(a)
            if result is None:
                continue
            value = self.max_value(result, 0, float('-inf'), float('inf'))

            if value > max_value:
                max_value = value
                max_a = a

        return max_a

    def max_value(self, state, depth, alpha, beta):
        if depth == 0:
            float('-inf')

        if state.is_terminal() or depth == self.depth:
            return state.utility()

        v = float('-inf')

        for s in state.successors():
            v = max(v, self.min_value(s, depth + 1, alpha, beta))
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v

    def min_value(self, state, depth, alpha, beta):
        if depth == 0:
            return float('inf')

        if state.is_terminal() or depth == self.depth:
            return state.utility()

        v = float('inf')
        for s in state.successors():
            v = min(v, self.max_value(s, depth + 1, alpha, beta))
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v
