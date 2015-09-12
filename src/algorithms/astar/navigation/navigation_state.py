""" Specialization of SearchState """
from src.algorithms.astar.search_state import SearchState
from src.algorithms.astar.navigation.navigation_grid import NavigationGrid
from src.algorithms.astar.navigation.utils.const import C
from src.algorithms.astar.navigation.utils.id_generator import ID_GENERATOR


class NavigationState(SearchState):
    """ A navigation, containing the state of the map as a NavigationGrid """

    def create_state_identifier(self):
        return ID_GENERATOR.get_id(self.state.position_string())

    def heuristic_evaluation(self):
        return self.state.distance_from_goal()

    def is_solution(self):
        return self.state.is_on_goal()

    def solution_length(self):
        return self.state.visited_len()

    def generate_all_successors(self):
        viable_movements = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        successors = []

        for move in viable_movements:
            pos = self.state.current_pos
            x_dim = self.state.map.x_dim()
            y_dim = self.state.map.y_dim()

            next_pos = [pos[0] - move[0], pos[1] - move[1]]
            x = next_pos[0]
            y = y_dim - next_pos[1] - 1

            if x < 0 or x > (x_dim - 1):
                continue

            if y < 0 or y > (y_dim - 1):
                continue

            if self.state.map.grid[y][x] == C.OBSTACLE:
                continue

            if self.state.is_visited(next_pos):
                continue

            visited = self.state.visited_copy() + [next_pos]

            successor = NavigationState(
                NavigationGrid(self.state.map, visited, next_pos)
            )

            successors.append(successor)

        return successors

    def print_level(self):
        """ Prints map as text, with visited tiles marked """
        x_dim = self.state.map.x_dim()
        y_dim = self.state.map.y_dim()

        output = [[0] * x_dim for _ in range(y_dim)]

        for pos in self.state.visited_copy():
            output[y_dim - pos[1] - 1][pos[0]] = 1

        for i, row in enumerate(self.state.map.grid):
            for j, element in enumerate(row):
                if element is C.OBSTACLE:
                    output[i][j] = C.PRINT_OBSTACLE

        print '\n'.join([' '.join([str(el) for el in row]) for row in output])
