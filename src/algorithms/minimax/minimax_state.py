""" A minimax search state, keeps a depth, parent and children nodes. How the children is being generated and the
heuristic evaluation has to be implemented in a subclass of this MinimaxState class.
"""


class MinimaxState(object):
    """ A search state contains a representation of a minimax state. """

    def __init__(self, state):
        self.state = state # An object describing a state of the search process
        self.sid = self.create_state_identifier()
        self.depth = None
        self.is_maxnode = False

        self.parent = None  # Pointer to the parent node
        self.kids = []  # All children to this node

    def heuristic_evaluation(self):
        """ Returns an estimate of distance to goal """
        raise NotImplementedError(
            'Implement compute_h() in SearchState subclass')

    def create_state_identifier(self):
        """ Creates a unique id based on state """
        raise NotImplementedError(
            'Implement create_state_identifier() in SearchState subclass')

    def generate_children(self):
        """ Generate a list of successors """
        raise NotImplementedError(
            'Implement generate_all_successors() in SearchState subclass')

    def add_child(self, child):
        """ Add a child to this node """
        self.kids.append(child)

    def set_parent(self, parent):
        self.parent = parent

    def set_depth(self, depth):
        self.depth = depth
