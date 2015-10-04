from src.algorithms.gac.constraint import Constraint
from src.algorithms.gac.func import make_function


class VertexConstraint(Constraint):

    def __init__(self, expression=None):
        Constraint.__init__(self)

        self.expression = expression
        self.parse_vars()
        self.create_func()

    def create_func(self):
        self.function = make_function(self.variables, self.expression)

    def revise(self, v, c, domains):
        to_remove = []
        for variable in c.variables:
            if v is variable:
                continue

            for d1 in domains[v]:
                removable = True
                for d2 in domains[variable]:
                    if c.function(d1, d2):
                        removable = False

                if removable:
                    to_remove.append(d1)

        if to_remove:
            domains[v] = [e for e in domains[v] if not e in to_remove]
        return len(to_remove) > 0

    def parse_vars(self):
        self.variables = list(i for i in self.expression.split() if i != '!=')
