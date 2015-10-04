""" An implementation of one of the traditional CSP algorithms:
General Arc Consistency. """
from collections import defaultdict


class GAC(object):
    """ GAC class containing the domain and queue, with the methods for
    filtering the domain, and rerunning with assumptions. """
    def __init__(self):
        self.variable_map = defaultdict(list)  # variable => list of constraints
        self.queue = []  # tuples (variable, constraint)
        self.domains = {}  # variable => list of domains

    def initialize(self, domains, constraints):
        """ GAC initialize, set domains and populate variable_map and queue """
        self.domains = domains

        for c in constraints:
            for v in c.variables:
                self.variable_map[v].append(c)
                self.queue.append((v, c))

    def domain_filtering(self):
        """ Filters domains by calls to revise """
        while self.queue:
            v, c = self.queue.pop(0)

            if self.revise(v, c):
                if len(self.domains[v]) == 0:
                    return False

                for constraint in set(self.variable_map[v]):
                    for neighbor in constraint.variables:
                        if neighbor != v:
                            self.queue.append((neighbor, constraint))
        return True

    def revise(self, v, c):
        """ Delegates the revise call to the constraint implementation. """
        return c.revise(v, c, self.domains)

    def rerun(self, domains, assumption):
        """ Reruns domain filtering with a new domain and a given assumption """
        self.domains = domains
        self.add_to_queue(assumption)
        return self.domain_filtering()

    def add_to_queue(self, v):
        """ Adds constraints for a given variable to the queue. """
        for constraint in set(self.variable_map[v]):
            for neighbor in constraint.variables:
                self.queue.append((neighbor, constraint))
