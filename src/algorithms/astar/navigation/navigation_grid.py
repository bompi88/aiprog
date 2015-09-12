""" The navigation grid contains a map and can be contained by states """
from copy import deepcopy


class NavigationGrid(object):
    """ A convenience class for holding a navigation map. The map is a tuple,
     which cannot be mutated, we only keep track of visited tiles.
    """
    def __init__(self, map_, visited=None, current_pos=None):
        self.map = map_
        self.__visited = visited or [map_.start]
        self.current_pos = current_pos or map_.start

    def position_string(self):
        """ Returns a string of the current tile """
        return ','.join([str(el) for el in self.current_pos])

    def visited_copy(self):
        """ Returns a deepcopy of the list of visited tiles """
        return deepcopy(self.__visited)

    def visited_len(self):
        """ Returns length of current path """
        return len(self.__visited)

    def is_visited(self, pos):
        """ Check whether pos in on current path """
        return pos in self.__visited

    def add_visited(self, pos):
        """ Adds position to current path """
        self.__visited.append(pos)

    def is_on_goal(self):
        """ Is the current tile the goal tile """
        return self.map.goal == self.current_pos

    def distance_from_goal(self):
        """ Returns the euclidean distance from the goal to current tile.
         Euclidean distance gave better results on some boards vs. manhattan
        """
        return self.euclidean_distance(self.map.goal, self.current_pos)

    @classmethod
    def euclidean_distance(cls, a, b):
        """ sqrt(x^2 + y^2) """
        x = (b[0] - a[0]) ** 2
        y = (b[1] - a[1]) ** 2

        return (x + y) ** 0.5
