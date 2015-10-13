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
            # print(state.evaluation_function())
            return state.evaluation_function()

        v = float('-inf')

        for successor in state.generate_successors(True):
            v = max(v, self.min_value(successor, alpha, beta, depth - 1))

            alpha = max(alpha, v)

            if v >= beta:
                break

        return v

    def min_value(self, state, alpha, beta, depth):
        if state.cutoff_test(depth):
            # print(state.evaluation_function())
            return state.evaluation_function()

        v = float('inf')

        for successor in state.generate_successors(False):
            v = min(v, self.max_value(successor, alpha, beta, depth - 1))

            beta = min(beta, v)

            if v <= alpha:
                break

        return v
