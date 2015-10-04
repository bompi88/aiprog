""" GAC constraint superclass """
from copy import deepcopy

from src.utils.func import make_function


class Constraint(object):
    """ Object holding an expression with variables, and implements
    a revise method tailored to the problem. """

    def __init__(self, expression):
        self.variables = []
        self.expression = None
        self.function = None

        self.gen_expressions(expression)
        self.parse_vars()
        self.create_func()

    def create_func(self):
        """ Creates functions for variables and expression.
        Handles one and two variables. """
        self.function = {
            self.variables[0]: make_function(self.variables, self.expression[0])
        }

        if len(self.variables) > 1:
            function = make_function(self.variables, self.expression[1])
            self.function[self.variables[1]] = function

    def revise(self, v, domains):
        """ Implements revise(). Works for one and two variables """
        if v == self.variables[0]:
            if len(self.variables) > 1:
                return self.reduce(self.variables[0],
                                   self.variables[1],
                                   domains)
            else:
                return self.reduce(self.variables[0], None, domains)
        elif v == self.variables[1]:
            return self.reduce(self.variables[1], self.variables[0], domains)

    def reduce(self, v1, v2, domains):
        """ Helper method for revise in pruning domains. """
        revised = False
        want_new = True

        for d1 in domains[v1]:
            satisfied = False
            if v2:
                for d2 in domains[v2]:
                    if self.function[v1](d1, d2):
                        satisfied = True
                        break
            else:
                if self.function[v1](d1):
                    satisfied = True
            if not satisfied:
                if want_new:
                    domains[v1] = deepcopy(domains[v1])
                    want_new = False
                domains[v1].remove(d1)
                revised = True

        return revised

    def parse_vars(self):
        """ Creates variables from constraint """
        raise NotImplementedError(
            'Implement parse_vars() in Constraint subclass')

    def gen_expressions(self, expression):
        """ Generates the expressions to create functions of """
        raise NotImplementedError(
            'Implement gen_expressions() in Constraint subclass')
