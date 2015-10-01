from collections import defaultdict
from copy import deepcopy


class GAC(object):
    def __init__(self):
        self.variable_map = defaultdict(list)  # variable => list of constraint ids
        self.queue = []  # tuples (variable, constraint)
        self.domains = {}  # variable => list of domains

    def initialize(self, domains, constraints):
        self.domains = domains

        for c in constraints:
            for v in c.variables:
                self.variable_map[v].append(c)
                self.queue.append((v, c))

    def domain_filtering(self):
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
        want_new = True

        for variable in c.variables:
            if v != variable and len(self.domains[variable]) == 1 and self.domains[variable][0] in self.domains[v]:
                if want_new:
                    self.domains[v] = deepcopy(self.domains[v])
                    want_new = False

                self.domains[v].remove(self.domains[variable][0])
                return True
        return False

    def rerun(self, domains, assumption):
        self.domains = domains
        self.add_to_queue(assumption)
        return self.domain_filtering()

    def add_to_queue(self, v):
        for constraint in set(self.variable_map[v]):
            for neighbor in constraint.variables:
                self.queue.append((neighbor, constraint))
