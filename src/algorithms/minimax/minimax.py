""" Super class for minimax solver, that implements Minimax algorithm and some helper methods."""


class Minimax(object):
    """ Implementation of Minimax. Contains methods that raise NotImplementedError,
    so should be treated as an abstract base class.
    """

    def __init__(self, start, max_depth, gui=None):
        self.start = start
        self.max_depth = max_depth
        self.gui = gui
        self.depth_to_nodes = {}

    def expand_until_depth(self, parent, current_depth, max_depth):
        """
        :param parent: Parent node
        :param current_depth: which level node is on
        :param max_depth: maximum depth to expand to
        :return:
        """
        children = parent.generate_children()
        self.depth_to_nodes[current_depth] = []

        for child in children:
            child.set_parent(parent)
            child.set_depth(current_depth)

            self.depth_to_nodes[current_depth].append(child)

            if current_depth < max_depth:
                return self.expand_until_depth(child, current_depth + 1, max_depth)

            return True

    def expand_tree(self):
        self.depth_to_nodes[0] = [self.start]
        self.expand_until_depth(self.start, 0, self.max_depth)
