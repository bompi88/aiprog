from src.algorithms.gac.constraint import Constraint
from src.algorithms.gac.func import make_function
from copy import deepcopy


class VertexConstraint(Constraint):

    def __init__(self, expression=None):
        Constraint.__init__(self)

        self.expression = expression
        self.parse_vars()
        self.create_func()

    def create_func(self):
        self.function = make_function(self.variables, self.expression)

    def revise(self, v, c, domains):
        want_new = True

        for variable in c.variables:
            if v != variable and len(domains[variable]) == 1 and domains[variable][0] in domains[v]:
                if want_new:
                    domains[v] = deepcopy(domains[v])
                    want_new = False

                domains[v].remove(domains[variable][0])
                return True
        return False

    def parse_vars(self):
        self.variables = list(i for i in self.expression.split() if i != '!=')
