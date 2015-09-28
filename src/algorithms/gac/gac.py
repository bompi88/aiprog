from copy import deepcopy


class GAC(object):
    def __init__(self):
        self.variable_map = {}  # variable => list of constraint ids
        self.constraint_map = {}  # constraint_id => list of vars
        self.queue = []  # tuples (variable, constraint)
        self.functions = {} # constraint_id => (f(x, y), f(y, x))
        self.domains = {}  # variable => list of domains

        self.constraints = {} # Key: constraint_id, Value: c1, c2

    def initialize(self, variables, domains, constraints):
        self.domains = domains

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

    def revise_star(self, var_cons_pair):
        variable = var_cons_pair[0]
        original_domain_size = len(self.domains[variable])
        constraint_id, c1, c2 = var_cons_pair[1]

        to_remove = []
        vars_to_consider = deepcopy(self.constraint_map[constraint_id])
        vars_to_consider.remove(variable)

        # For all values in focus variable's domain
        for d1 in self.domains[variable]:
            retain = False

            funcs = self.functions[constraint_id]

            for v in vars_to_consider:
                for d2 in self.domains[v]:
                    if c1[:2] == v:
                        try:
                            if funcs[0](d1, d2):
                                retain = True
                        except:
                            pass
                    else:
                        try:
                            if funcs[1](d2, d1):
                                retain = True
                        except:
                            pass

            if not vars_to_consider and funcs[0](d1):
                retain = True

            if not retain:
                to_remove.append(d1)

        self.domains[variable] = [
            e for e in self.domains[variable] if e not in to_remove
        ]

        if len(self.domains[variable]) is 1:
            for el in self.queue:
                if el[0] is variable:
                    self.queue.remove(el)

        # if domain gets reduced, return true
        return len(self.domains[variable]) < original_domain_size

    def rerun(self, domain, assumption):
        self.domains = domain
        self.add_to_queue(assumption)
        self.domain_filtering()

    def add_to_queue(self, objective, exclude=False):
        # All constraints that has to be rechecked
        var = objective[0]
        constraints = set(self.variable_map[var])

        # All affected variables
        variable_lists = [self.constraint_map[c] for c in constraints]
        variables = set([el for row in variable_lists for el in row]) # Flatten

        objective_id = objective[1][0]

        for v in variables:
            cs = self.variable_map[v]

            for c_id in cs:
                # Do not consider the last revised constraint
                if exclude and c_id is objective_id:
                    continue
                else:
                    c1, c2 = self.constraints[c_id]
                    self.queue.append((v, (c_id, c1, c2)))

    @staticmethod
    def make_function(variable_names, expression, environment=globals()):
        arguments = ','.join([variable for variable in variable_names])
        statement = '(lambda {}: {})'.format(arguments, expression)

        return eval(statement, environment) # pylint: disable=eval-used
