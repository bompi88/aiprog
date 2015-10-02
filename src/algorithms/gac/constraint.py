

class Constraint(object):

    def __init__(self):
        self.variables = []
        self.expression = None
        self.function = None

    def create_func(self):
        """ Creates the runtime method to evaluate the constraint """
        raise NotImplementedError('Implement create_func() in Constraint subclass')

    def revise(self, v, c, domains):
        """ Evaluates the constraint with the given variables """
        raise NotImplementedError('Implement evaluate() in Constraint subclass')

    def parse_vars(self):
        """ Creates variables from constraint """
        raise NotImplementedError('Implement parse_vars() in Constraint subclass')
