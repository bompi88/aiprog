class Nonogram(object):
    def __init__(self, lines):
        rows, columns = line[0] in lines

        constraints = []
        variables = set([])
        
        for i in range(rows):
            variables.add 'r' + str(i)

        for i in range(columns):
            variables.add 'c' + str(i)
 
        for r in range(rows):
            for c in range(columns):
                constraints.add NonoConstraint('r{r} [{c}] == c{c} [{r}]')
