""" A GAC constraint class for our simple example """
from src.algorithms.gac.constraint import Constraint


class SimpleConstraint(Constraint):
    """ Handles constraints of one or two variables with a simple
    boolean expression between them
    """

    def __init__(self, expression, valid_variables):
        self.valid = valid_variables

        Constraint.__init__(self, expression)

    def parse_vars(self):
        expression_list = self.expression[0].split()
        self.variables = [i for i in expression_list if i in self.valid]

    def gen_expressions(self, expression):
        parts = expression.split()

        self.expression = [
            expression,
            parts[2] + ' ' + parts[1] + ' ' + parts[0]
        ]
