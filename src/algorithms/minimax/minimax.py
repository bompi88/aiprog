class Minimax(object):
    def __init__(self, actions, depth):
        self.actions = actions
        self.depth = depth

    def alpha_beta_decision(self, state):
        max_value = float('-inf')
        max_a = None

        for a in self.actions:
            result = state.perform(a)
            if result is None:
                continue
            value = self.max_value(result, float('-inf'),
                                   float('inf'), self.depth)

            if value > max_value:
                max_value = value
                max_a = a

        return max_a

    def max_value(self, state, alpha, beta, depth):
        if state.cutoff_test(depth):
            return state.evaluation_function()

        v = float('-inf')

        for s in state.successors():
            v = max(v, self.min_value(s, alpha, beta, depth - 1))

            if v >= beta:
                return v

            alpha = max(alpha, v)

        return v

    def min_value(self, state, alpha, beta, depth):
        if state.cutoff_test(depth):
            return state.evaluation_function()

        v = float('inf')
        for s in state.successors():
            v = min(v, self.max_value(s, alpha, beta, depth - 1))

            if v >= alpha:
                return v

            beta = max(beta, v)

        return v
