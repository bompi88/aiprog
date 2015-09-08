from collections import namedtuple

arc_cost = 0.8

Constants = namedtuple('Constants', [
    'TILE',
    'OBSTACLE',
    'START',
    'GOAL',
    'PRINT_OBSTACLE',
    'ARC_COST'
])

const = Constants(
    1,
    2,
    3,
    4,
    '#',
    arc_cost
)
