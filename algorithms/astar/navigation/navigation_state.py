import copy

from algorithms.astar.search_state import SearchState
from algorithms.astar.navigation.navigation_grid import NavigationGrid
from algorithms.astar.navigation.const import *

class NavigationState(SearchState):
    def create_state_identifier(self):
        flattened_visited = [str(el) for row in self.state.visited for el in row]
        return ''.join(flattened_visited)

    @classmethod
    def manhattan_distance(self, a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    def heuristic_evaluation(self):
        return self.manhattan_distance(
            self.state.current_pos,
            self.state.goal()
        )

    def is_solution(self):
        pos = self.state.current_pos
        goal = self.state.goal()

        return tuple(pos) == goal

    def solution_length(self):
        return len(self.state.visited)

    def generate_all_successors(self, generated):
        viable_movements = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        successors = []

        for move in viable_movements:
            pos   = self.state.current_pos
            x_dim = self.state.x_dim()
            y_dim = self.state.y_dim()

            next_pos = [pos[0] - move[0], pos[1] - move[1]]
            x        = next_pos[0]
            y        = y_dim - next_pos[1] - 1

            if x < 0 or x > (x_dim - 1):
                continue

            if y < 0 or y > (y_dim - 1):
                continue

            if self.state.grid[y][x] == const.OBSTACLE:
                continue

            if next_pos in self.state.visited:
                continue

            visited = copy.deepcopy(self.state.visited)
            visited.append(next_pos)
            successor = NavigationState(
                NavigationGrid(self.state.map, self.state.grid, visited)
            )

            successor.id = successor.create_state_identifier()
            successor.state.current_pos = next_pos

            successors.append(successor)
            generated[successor] = successor

        return successors

    def print_level(self):
        rows = []

        grid  = self.state.grid
        x_dim = self.state.x_dim()
        y_dim = self.state.y_dim()

        output = [0] * y_dim

        for i in range(x_dim):
            output[i] = [0] * y_dim

        for pos in self.state.visited:
            output[y_dim - pos[1] - 1][pos[0]] = 1

        for i, row in enumerate(grid):
            for j, el in enumerate(row):
                if el == const.OBSTACLE:
                    output[i][j] = const.PRINT_OBSTACLE

        for list in output:
            rows.append(' '.join(map(str, list)))

        print('\n'.join(rows) + '\n\n')
