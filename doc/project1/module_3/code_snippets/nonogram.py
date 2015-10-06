""" Pseudocode shortened implementation of the Nonogram
representation of variables and constraints """
class Nonogram(object):
    def __init__(self, lines):
        rows, columns = lines.first()

        constraints = []
        variables = set([])
        
        for i in range(rows):
            variables.add('r' + str(i))

        for i in range(columns):
            variables.add('c' + str(i))
 
        for r in range(rows):
            for c in range(columns):
                constraint = NonogramConstraint('r{r} [{c}] == c{c} [{r}]')
                constraints.append(constraint)
