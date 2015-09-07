import sys
import abc


class AstarNode(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, init_state):
        self.h_tmp = sys.maxint
        self.closed = False
        self.g = 0
        self.count = None
        self.state = init_state
        self.successors = []  # The successors of the node
        self.parents = []  # The parents

    def __cmp__(self, other):
        return cmp(self.f(), other.f())

    def f(self):
        if not self.count:
            return self.h() + self.g
        else:
            return self.count

    def __str__(self):
        return "h: {}, g: {}, f: {}".format(self.h_tmp, self.g, self.f())

    def is_sol(self):
        """Checks whether this is node is a solution"""
        return self.h == 0

    def gen_h(self):
        """Stores the current heuristics in a temporal variable"""
        self.h_tmp = self.h()

    def get_successors(self):
        """Returns the generated successors or generates new successors if not present"""
        if self.successors is not None:
            return self.successors

        self.successors = self.gen_suc()
        return self.successors

    def set_parent(self, parent):
        """Sets the new parent and updates the g value"""
        self.parents.append(parent)
        self.g = parent.g + self.h(parent)

    def is_better(self, other):
        """Checks if this instance is better than the other instance provided"""
        return other.g + self.h(other) < self.g

    @abc.abstractmethod
    def gen_suc(self):
        """Should generate the successors of this node"""
        return

    @abc.abstractmethod
    def gen_state(self):
        """Should generate a new state"""
        return

    @abc.abstractmethod
    def h(self, other):
        """Should contain the heuristic method"""
        return 0

    def id(self):
        """Should generate a id that represents the given state"""
        if self.state is None:
            self.state = self.gen_state()

        return self.state
