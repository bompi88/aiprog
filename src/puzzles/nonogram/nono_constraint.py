from src.algorithms.gac.constraint import Constraint
from src.algorithms.gac.func import make_function
from copy import deepcopy


class NonoConstraint(Constraint):

    def __init__(self, expression=None):
        Constraint.__init__(self)

        parts = expression.split()

        self.expression = [
            expression,
            parts[3] + ' ' + parts[1] + ' ' + parts[2] + ' ' + parts[0] + ' ' + parts[4]
        ]

        self.parse_vars()
        self.create_func()

    def create_func(self):
        self.function = {
            self.variables[0]: make_function(self.variables, self.expression[0]),
            self.variables[1]: make_function(self.variables, self.expression[1])
        }

    def revise(self, v, c, domains):
        if v == self.variables[0]:
            return self.reduce(self.variables[0], self.variables[1], domains)
        elif v == self.variables[1]:
            return self.reduce(self.variables[1], self.variables[0], domains)

    def reduce(self, v1, v2, domains):
        revised = False
        want_new = True

        for d1 in domains[v1]:
            satisfied = False
            for d2 in domains[v2]:
                if self.function[v1](d1, d2):
                    satisfied = True
                    break
            if not satisfied:
                if want_new:
                    domains[v1] = deepcopy(domains[v1])
                    want_new = False
                domains[v1].remove(d1)
                revised = True

        return revised

    def parse_vars(self):
        self.variables = [i for i in self.expression[0].split() if self.var(i)]

    def var(self, i):
        return i != '==' and i[0] != '['
