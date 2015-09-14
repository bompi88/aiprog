
class GAC(object):
    def __init__(self, state):
        self.queue = []
        self.domains = state.domains

    def initialize(self):
        return True

    def domain_filtering(self):
        todo_revise = self.queue.pop()
        return todo_revise

    def rerun(self):
        self.domain_filtering()

    @staticmethod
    def make_function(variable_names, expression, environment=globals()):
        arguments = ','.join([variable for variable in variable_names])
        statement = '(lambda {}: {})'.format(arguments, expression)

        return eval(statement, environment) # pylint: disable=eval-used
