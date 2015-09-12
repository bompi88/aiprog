""" Constants relevant for module, contains constants also defined
 in both algorithms/astar/const and algorithms/astar/navigation/const
"""

from collections import namedtuple

Constants = namedtuple(
    'Constants',
    ['TILE', 'OBSTACLE', 'START', 'GOAL', 'OPEN', 'CLOSED', 'NEW', 'A_STAR',
     'DFS', 'BFS', 'DEBUG', 'VERBOSE', 'SILENT']
)

C = Constants(1, 2, 3, 4, 1, 2, 3, 1, 2, 3, 1, 2, 3)
