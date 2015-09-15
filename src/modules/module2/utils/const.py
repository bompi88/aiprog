""" Constants relevant for module, contains constants also defined
 in both algorithms/astar/const and algorithms/astar/navigation/const
"""

from collections import namedtuple

Constants = namedtuple(
    'Constants',
    ['A_STAR', 'RED', 'GREEN', 'BLUE', 'ORANGE', 'WHITE', 'BLACK']
)

C = Constants(1, 1, 2, 3, 4, 5, 6)
