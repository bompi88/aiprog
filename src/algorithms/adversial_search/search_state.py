class SearchState(object):
    def cutoff_test(self, test):
        raise NotImplementedError(
            'Implement cutoff_test(test) in SearchState subclass')

    def perform(self, action):
        raise NotImplementedError(
            'Implement perform(action) in SearchState subclass')

    def generate_successors(self, is_max):
        raise NotImplementedError(
            'Implement successors() in SearchState subclass'
        )

    def evaluation_function(self):
        raise NotImplementedError(
            'Implement evaluation_function() in SearchState subclass'
        )
