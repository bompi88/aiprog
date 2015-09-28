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

        self.constraints = {} # Key: constraint_id, Value: c1, c2

    def initialize(self, variables, domains, constraints):
        self.domains = deepcopy(domains)

        for (id, c1, c2) in constraints:
            elements = c1.split()

            vars = list(set(elements) & set(variables))

            self.constraints[id] = (c1, c2)
            self.constraint_map[id] = vars

            for v in vars:
                if v in self.variable_map.keys():
                    self.variable_map[v].append(id)
                else:
                    self.variable_map[v] = [id]

                self.queue.append((v, (id, c1, c2)))

            self.functions[id] = (
                self.make_function(vars, c1),
                self.make_function(vars, c2)
            )

    def domain_filtering(self):
        while len(self.queue):
            todo_revise = self.queue.pop(0)

            if self.revise_star(todo_revise):
                self.add_to_queue(todo_revise, True)

        return self.domains

    def revise_star(self, cv_pair):
        # todo: add multiple variable support

        variable = cv_pair[0]
        constraint_id, c1, c2 = cv_pair[1]

        size_domain_old = len(self.domains[variable])

        vars_to_consider = deepcopy(self.constraint_map[constraint_id])
        vars_to_consider.remove(variable)

        to_remove = []

        # For all values in focus variable's domain
        for d1 in self.domains[variable]:
            retain = False

            if vars_to_consider and len(vars_to_consider) > 0:
                for d2 in self.domains[vars_to_consider[0]]:
                    var_order = c1.split()

                    if var_order[0] is variable:
                        if self.functions[constraint_id][0](d1, d2):
                            retain = True
                    else:
                        try:
                            if self.functions[constraint_id][1](d1, d2):
                                retain = True
                        except:
                            if self.functions[constraint_id][1](d2, d1):
                                retain = True
            else:
                if self.functions[constraint_id][0](d1):
                    retain = True

            if not retain and d1 in self.domains[variable]:
                to_remove.append(d1)

        if len(to_remove):
            self.domains[variable] = deepcopy(self.domains[variable])

        # Remove the values from the domain if
        for r in to_remove:
            self.domains[variable].remove(r)

        if len(self.domains[variable]) is 1:
            for el in self.queue:
                if el[0] is variable:
                    self.queue.remove(el)

        size_domain_new = len(self.domains[variable])

        # if domain gets reduced, return true
        return size_domain_new < size_domain_old

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

            for c_id in cs:
                # Do not consider the last revised constraint
                if exclude and c_id is objective[1]:
                    continue
                else:
                    c1, c2 = self.constraints[c_id]
                    self.queue.append((v, (c_id, c1, c2)))

    @staticmethod
    def make_function(variable_names, expression, environment=globals()):
        arguments = ','.join([variable for variable in variable_names])
        statement = '(lambda {}: {})'.format(arguments, expression)

        return eval(statement, environment) # pylint: disable=eval-used