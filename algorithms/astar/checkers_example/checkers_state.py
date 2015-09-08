__author__ = 'krisvage'

import copy
from algorithms.astar.search_state import SearchState

class CheckersState(SearchState):
    def create_state_identifier(self):
        return ''.join(map(str, [item for sublist in self.state for item in sublist]))

    @classmethod
    def manhattan_distance(self, a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    def heuristic_evaluation(self):
        manhattan_distance = 0

        correct_positions = {
             1: (0, 0),  2: (1, 0),  3: (2, 0),  4: (3, 0),  5: (4, 0),
             6: (0, 1),  7: (1, 1),  8: (2, 1),  9: (3, 1), 10: (4, 1),
            11: (0, 2), 12: (1, 2), 13: (2, 2), 14: (3, 2), 15: (4, 2),
            16: (0, 3), 17: (1, 3), 18: (2, 3), 19: (3, 3), 20: (4, 3),
            21: (0, 4), 22: (1, 4), 23: (2, 4), 24: (3, 4), 25: (4, 4)
        }

        for i, row in enumerate(self.state):
            for j, element in enumerate(row):
                correct_pos = correct_positions[element]
                actual_pos  = (j, i)

                distance = self.manhattan_distance(correct_pos, actual_pos)

                manhattan_distance += distance

        return manhattan_distance / 2

    def is_solution(self):
        return '12345678910111213141516171819202122232425' == self.id

    def solution_length(self):
        if self.parent is None:
            return 1
        else:
            return 1 + self.parent.solution_length()

    def generate_all_successors(self, generated):
        succs    = []
        original = self.state

        for i in range(5):
            for j in range(4):
                successor = copy.deepcopy(original)

                successor[i][j] = successor[i][j + 1]
                successor[i][j + 1] = original[i][j]

                successor_state = CheckersState(successor)
                generated[successor_state.id] = successor_state
                succs.append(successor_state)

        for i in range(5):
            for j in range(4):
                successor = copy.deepcopy(original)

                successor[j][i] = successor[j + 1][i]
                successor[j + 1][i] = original[j][i]

                successor_state = CheckersState(successor)
                generated[successor_state.id] = successor_state
                succs.append(successor_state)

        return succs

    def print_level(self):
        rows = []
        for list in self.state:
            rows.append(' '.join(map(str, list)))

        print('\n'.join(rows) + '\n\n')




