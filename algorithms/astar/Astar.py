from TraversalType import TraversalType
from AstarNode import AstarNode
from time import time, sleep
from Status import Status
import Queue as Q


class Astar(object):

    def __init__(self):
        self.status = Status.IDLE  # Current state of the search
        self.count = 0  # Node processed
        self.current = None  # Current processing node
        self.shuffle = False  # Shuffle the children or not
        self.start_node = None  # The initial node
        self.traversal_type = TraversalType.ASTAR  # Type of traversal (Breadth First, Depth First or Best First)
        self.start_time = 0  # Start time of the search loop
        self.elapsed_time = 0  # The elapsed time of the search
        self.delay = 10  # Milliseconds to delay each search iteration
        self.closed = 0  # Keep track of number of closed nodes

        self.generated = {}  # dictionary of processed nodes
        self.opened = None  # PriorityQueue for nodes yet to be processed

    def visualize_state(self, node):
        print node
        node.visualize()
        sleep(self.delay)
        node.devisualize()

    def stop(self):
        print "Stopping the search..."
        self.status = Status.IDLE

    def search(self, start, traversal_type):

        if not isinstance(start, AstarNode):
            print start, " is not of type AstarNode"
            return

        # Do some formal stuff
        self.start_node = start
        self.start_time = time()
        self.status = Status.RUNNING

        if type is not None:
            self.traversal_type = traversal_type

        # Initializing and resetting the Astar search
        start.gen_h()

        self.opened = Q.PriorityQueue()
        self.opened.put(start)

        self.count = 0
        self.closed = 0
        self.current = None

        # Run the Astar loop
        while not self.opened.empty():
            self.current = self.opened.get()

            self.visualize_state(self.current)
            self.current.closed = True
            self.closed += 1

            if self.status != Status.RUNNING:
                return self.current

            for successor in start.get_successors():
                # If identical node has already been calculated, use the old one
                if successor.id() in self.generated:
                    successor = self.generated[successor.id()]

                # If not already generated,
                if successor.id() not in self.generated:
                    self.generated[successor.id()] = successor
                    self.attach_and_evaluate(successor, self.current)

                    if self.traversal_type is TraversalType.BFS:
                        self.count += 1
                        successor.count = self.count
                    elif self.traversal_type is TraversalType.DFS:
                        self.count -= 1
                        successor.count = self.count
                    self.opened.put(successor)

                elif successor.isBetter(self.current):
                    # Else if successor is better than parent, attach and evaluate and update the search tree
                    self.attach_and_evaluate(successor, self.current)
                    if successor.closed:
                        self.prop_path_imp(successor)

                self.current.successors.put(successor)

            self.elapsed_time = time() - self.start_time

        # If no solution, tag it and return the current best node
        self.status = Status.NO_SOLUTION
        self.elapsed_time = time() - self.start_time

        return self.current

    def attach_and_evaluate(self, successor, parent):
        """Should set new parent and generate the heuristics"""
        successor.setParent(parent)
        successor.gen_h()

    def prop_path_imp(self, parent):
        """Update all children references"""
        for child in parent.children:
            if child.is_better(parent):
                child.set_parent(parent)
                self.prop_path_imp(child)

    def num_opened(self):
        """Computes the number of opened nodes."""
        return self.num_generated() + self.num_closed()

    def num_closed(self):
        """Computes the number of closed nodes."""
        return self.closed

    def num_generated(self):
        """Returns number of nodes that has been generated"""
        return len(self.generated)

    def __str__(self):
        return "type: {}, generated: {}, opened: {}, closed: {}, elapsed time: {}"\
            .format(self.traversal_type, self.num_closed(), self.num_closed(), self.elapsed_time)
