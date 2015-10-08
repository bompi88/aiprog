class MinimaxState(object):
    def cutoff_test(self, test):
        raise NotImplementedError(
            'Implement cutoff_test(test) in MinimaxState subclass')

    def perform(self, action):
        raise NotImplementedError(
            'Implement perform(action) in MinimaxState subclass')

    def successors(self):
        raise NotImplementedError(
            'Implement successors() in MinimaxState subclass'
        )

    def evaluation_function(self):
        raise NotImplementedError(
            'Implement evaluation_function() in Minimax subclass'
        )
