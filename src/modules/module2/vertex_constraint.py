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

    def evaluate(self, focus_var, focus_val, other_var, domains):
        return focus_val not in domains[other_var]

    def parse_vars(self):
        self.variables = list(i for i in self.expression.split() if i != '!=')
