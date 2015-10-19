class Expectimax(object):
    def __init__(self, actions, depth):
        self.actions = actions
        self.depth = depth

    def decision(self, state):
        max_value = float('-inf')
        max_a = None

        for a in self.actions:
            result = state.perform(a)

            if result is None:
                continue

            value = self.max_value(result, self.depth)

            if value > max_value:
                max_value = value
                max_a = a

        return max_a

    def max_value(self, state, depth):
        if state.cutoff_test(depth):
            return state.evaluation_function()

        v = float('-inf')

        for successor in state.generate_successors(True):
            v = max(v, self.chance_value(successor, depth - 1))

        return v

    def chance_value(self, state, depth):
        if state.cutoff_test(depth):
            return state.evaluation_function()

        vs = []

        for i, successor in enumerate(state.generate_successors(False)):
            probability = 0.9 if state.successor_tiles[i] is 1 else 0.1
            v = probability * self.max_value(successor, depth - 1)
            vs.append(v)

        return sum(vs) / len(vs)
