""" A GAC constraint class for our simple example """
from src.algorithms.gac.constraint import Constraint
from src.algorithms.gac.func import make_function


class SimpleConstraint(Constraint):
    """ Handles constraints of one or two variables with a simple
    boolean expression between them
    """

    def __init__(self, expression, valid_variables):
        Constraint.__init__(self)

        self.valid = valid_variables
        self.expression = expression
        self.parse_vars()
        self.create_func()


    def create_func(self):
        self.function = make_function(self.variables, self.expression)

    def parse_vars(self):
        self.variables = [i for i in self.expression.split() if i in self.valid]

    def revise(self, v, c, domains):
        if len(c.variables) is 1:
            return self.revise_single_var_expression(v, c, domains)
        else:
            return self.revise_multi_var_expression(v, c, domains)

    @staticmethod
    def revise_single_var_expression(v, c, domains):
        """ Revises an expression of the form 'v == 2' """
        revised = False
        for element in domains[v]:
            if not c.function(element):
                domains[v].remove(element)
                revised = True

        return revised

    @staticmethod
    def revise_multi_var_expression(v, c, domains):
        """ Revises an expression of the form v1 != v2 """
        to_remove = []
        for variable in c.variables:
            if v is variable:
                continue

            for element1 in domains[v]:
                removable = True
                for element2 in domains[variable]:
                    if c.function(element1, element2):
                        removable = False

                if removable:
                    to_remove.append(element1)

        if to_remove:
            domains[v] = [e for e in domains[v] if not e in to_remove]
        return len(to_remove) > 0
