from enum import Enum

# Have to install Enum:
# $ pip install enum34


class TraversalType(Enum):
    DFS = 0
    BFS = 1
    ASTAR = 2
