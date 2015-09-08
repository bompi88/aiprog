__author__ = 'krisvage'

OPEN   = 0
CLOSED = 1

class SearchState:
    def __init__(self, state):
        self.state = state # An object describing a state of the search process
        self.id    = self.create_state_identifier()
        self.g     = None # Cost of getting to this node
        self.h     = None # Estimated cost to goal
        self.f     = None # Estimated total cost of a solution path going
                          # through this node; f = g + h

        self.status = OPEN    # OPEN / CLOSED
        self.parent = None # Pointer to best parent node
        self.kids   = []   # list of all successor nodes, whether or not this
                           # node is currently their best parent.

    def heuristic_evaluation(self):
        raise NotImplementedError('Implement compute_h() in SearchState subclass')

    def create_state_identifier(self):
        raise NotImplementedError('Implement create_state_identifier() in SearchState subclass')

    def generate_all_successors(self, generated):
        raise NotImplementedError('Implement generate_all_successors() in SearchState subclass')

    def is_solution(self):
        raise NotImplementedError('Implement is_solution() in SearchState subclass')

    def solution_length(self):
        raise NotImplementedError('Implement solution_length in SearchState subclass')

    def add_child(self, child):
        self.kids.append(child)