""" Vertex specialization of Constraint """
from src.algorithms.gac.constraint import Constraint


class VertexConstraint(Constraint):
    """ Handles vertex constraints of the type v1 != v2 """
    def __init__(self, expression=None):
        Constraint.__init__(self, expression)

    def parse_vars(self):
        self.variables = [i for i in self.expression[0].split() if i != '!=']

    def gen_expressions(self, expression):
        parts = expression.split()

        self.expression = [
            expression,
            parts[2] + ' ' + parts[1] + ' ' + parts[0]
        ]
