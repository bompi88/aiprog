from copy import deepcopy
import itertools
import inspect


class GAC(object):

    def __init__(self):
        self.variable_map = {}  # Key: variable, Value: all constraints which includes this variable
        self.constraint_map = {}  # Key: expression/constraint, Value: all variables in this constraint
        self.queue = []  # tuples (variable, expression/constraint)
        self.functions = {} # Key: expression/constraint, Value: method to evaluate constraint
        self.domains = {}  # Key: variable, Value: List of available values that represent the domain of the variable

    def initialize(self, variables, domains, constraints):
        self.domains = deepcopy(domains)

        for c in constraints:
            elements = c.split()

            vars = list(set(elements) & set(variables))

            self.constraint_map[c] = vars

            for v in vars:
                if v in self.variable_map.keys():
                    self.variable_map[v].append(c)
                else:
                    self.variable_map[v] = [c]

                self.queue.append((v, c))

            self.functions[c] = self.make_function(vars, c)

    def domain_filtering(self):
        while len(self.queue):
            todo_revise = self.queue.pop(0)

            if self.revise_star(todo_revise):
                self.add_to_queue(todo_revise, True)

        return self.domains

    def revise_star(self, cv_pair):
        # todo: add multiple variable support

        size_domain_old = len(self.domains[cv_pair[0]])

        vars_to_consider = deepcopy(self.constraint_map[cv_pair[1]])
        vars_to_consider.remove(cv_pair[0])

        to_remove = []

        # For all values in focus variable's domain
        for d1 in self.domains[cv_pair[0]]:
            retain = False

            if vars_to_consider and len(vars_to_consider) > 0:
                for d2 in self.domains[vars_to_consider[0]]:
                    var_order = cv_pair[1].split()

                    if var_order[0] is cv_pair[0]:
                        if self.functions[cv_pair[1]](d1, d2):
                            retain = True

                    # TODO: Document in report or fix
                    else:
                        if self.functions[cv_pair[1]](d2, d1):
                                retain = True
            else:
                if self.functions[cv_pair[1]](d1):
                    retain = True

            if not retain and d1 in self.domains[cv_pair[0]]:
                to_remove.append(d1)

        # Remove the values from the domain if
        for r in to_remove:
            self.domains[cv_pair[0]].remove(r)

        if len(self.domains[cv_pair[0]]) is 1:
            for el in self.queue:
                if el[0] is cv_pair[0]:
                    self.queue.remove(el)

        size_domain_new = len(self.domains[cv_pair[0]])

        # if domain gets reduced, return true
        if size_domain_new < size_domain_old:
            return True
        else:
            return False

    def rerun(self, domain, assumption):
        self.domains = domain
        self.add_to_queue(assumption)
        self.domain_filtering()

    def add_to_queue(self, objective, exclude=False):
        # All constraints that has to be rechecked
        constraints = set(self.variable_map[objective[0]])

        # all affected variables
        variables = set(itertools.chain(*[self.constraint_map[c] for c in constraints]))

        for v in variables:
            cs = self.variable_map[v]

            for c in cs:
                # Do not consider the last revised constraint
                if exclude and c is objective[1]:
                    continue
                else:
                    self.queue.append((v, c))

    @staticmethod
    def make_function(variable_names, expression, environment=globals()):
        arguments = ','.join([variable for variable in variable_names])
        statement = '(lambda {}: {})'.format(arguments, expression)

        return eval(statement, environment) # pylint: disable=eval-used