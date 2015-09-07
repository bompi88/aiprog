from enum import Enum

# Have to install Enum:
# $ pip install enum34


class Status(Enum):
    IDLE = 0
    RUNNING = 1
    NO_SOLUTION = 2

