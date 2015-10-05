def make_function(variable_names, expression, environment=globals()):
  arguments = ','.join([variable for variable in variable_names])
  statement = '(lambda {}: {})'.format(arguments, expression)
  return eval(statement, environment)