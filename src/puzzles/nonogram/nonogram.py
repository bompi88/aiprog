""" Represent a nonogram """
from src.puzzles.nonogram.nonogram_constraint import NonogramConstraint


class Nonogram(object):
    """ Parses lines from a Nonogram file and creates constraints. """
    def __init__(self, lines):
        self.x, self.y = [int(e) for e in lines[0].split(' ')]
        self.rows, self.columns = None, None

        self.init_rows_and_columns(lines)

        self.constraints = []
        self.variables = set([])
        self.init_variables_and_constraints()

    def init_rows_and_columns(self, lines):
        """ Sets rows and columns based on lines """
        start, end = 1, 1+self.y
        rows = lines[start:end]
        start, end = end, end+self.x
        cols = lines[start:end]

        self.rows = [[int(n) for n in row.split(' ')] for row in rows]
        self.columns = [[int(n) for n in col.split(' ')] for col in cols]

    def init_variables_and_constraints(self):
        """ Adds variables and constraints to self """
        for i in range(self.y):
            self.variables.add('r' + str(i))

        for i in range(self.x):
            self.variables.add('c' + str(i))

        constraint_template = 'r{r} [{c}] == c{c} [{r}]'
        for y in range(self.y):
            for x in range(self.x):
                self.constraints.append(
                    NonogramConstraint(constraint_template.format(r=y, c=x))
                )
