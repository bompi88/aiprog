""" Constants relevant for the navigation maps """

from collections import namedtuple

Constants = namedtuple(
    'Constants',
    ['TILE', 'OBSTACLE', 'START', 'GOAL', 'PRINT_OBSTACLE']
)

C = Constants(1, 2, 3, 4, '#')
