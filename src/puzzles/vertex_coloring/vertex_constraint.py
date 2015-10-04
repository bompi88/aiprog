from src.algorithms.gac.constraint import Constraint


class VertexConstraint(Constraint):

    def __init__(self, expression=None):
        Constraint.__init__(self, expression)

    def parse_vars(self):
        self.variables = [i for i in self.expression[0].split() if self.var(i)]

    def var(self, i):
        return i != '!='

    def gen_expressions(self, expression):
        parts = expression.split()

        self.expression = [
            expression,
            parts[2] + ' ' + parts[1] + ' ' + parts[0]
        ]
