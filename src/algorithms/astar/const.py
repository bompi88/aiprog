""" Constants relevant for A* """

from collections import namedtuple

Constants = namedtuple(
    'Constants',
    ['OPEN', 'CLOSED', 'NEW', 'A_STAR', 'DFS', 'BFS', 'DEBUG', 'VERBOSE',
     'SILENT', 'TEST']
)

C = Constants(1, 2, 3, 1, 2, 3, 1, 2, 3, 4)
