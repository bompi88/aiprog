""" Represent a nonogram """
from src.puzzles.nonogram.nono_constraint import NonoConstraint


class Nonogram(object):
    # pylint: disable=too-many-instance-attributes

    def __init__(self, lines):
        self.x, self.y = [int(e) for e in lines[0].split(' ')]

        s, e = 1, 1+self.y
        self.rows = [[int(n) for n in row.split(' ')] for row in lines[s:e]]
        s, e = e, e+self.x
        self.columns = [[int(n) for n in col.split(' ')] for col in lines[s:e]]

        self.constraints = []
        self.variables = set([])
        self.init_constraints_and_variables()

    def init_constraints_and_variables(self):
        for i in range(self.y):
            self.variables.add('r' + str(i))

        for i in range(self.x):
            self.variables.add('c' + str(i))

        constraint_template = 'r{r} [{c}] == c{c} [{r}]'
        for y in range(self.y):
            for x in range(self.x):
                self.constraints.append(
                    NonoConstraint(constraint_template.format(r=y, c=x))
                )
