"""  Nonogram specialization of Constraint """
from src.algorithms.gac.constraint import Constraint


class NonogramConstraint(Constraint):
    """ Takes care of properly inversing Nonogram expressions """
    def __init__(self, expression=None):
        Constraint.__init__(self, expression)

    def parse_vars(self):
        self.variables = [i for i in self.expression[0].split() if self.var(i)]

    @staticmethod
    def var(i):
        """ Strings containing '==' or a list lookup are invalid variables. """
        return i != '==' and i[0] != '['

    def gen_expressions(self, expression):
        parts = expression.split()
        rev_expr = ' '.join([parts[3], parts[1], parts[2], parts[0], parts[4]])

        self.expression = [expression, rev_expr]
