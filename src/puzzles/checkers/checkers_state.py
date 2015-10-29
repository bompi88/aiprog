""" Represent a state of the 25-Checkers problem """
import copy
from src.algorithms.astar.search_state import SearchState


class CheckersState(SearchState):
    """ Inherit SearchState and override NotImplemented methods """

    def create_state_identifier(self):
        return ''.join([str(item) for row in self.state for item in row])

    @classmethod
    def manhattan_distance(cls, a, b):
        """ Distance between a and b when diagonal moves are disallowed """
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    def heuristic_evaluation(self):
        manhattan_distance = 0
        solution = {(1 + x + 5*y): (x, y) for x in range(5) for y in range(5)}

        for i, row in enumerate(self.state):
            for j, element in enumerate(row):
                correct = solution[element]
                position = (j, i)

                manhattan_distance += self.manhattan_distance(correct, position)

        return manhattan_distance / 2

    def is_solution(self):
        return self.h is 0

    def solution_length(self):
        if self.parent is None:
            return 1
        else:
            return 1 + self.parent.solution_length()

    def generate_all_successors(self):
        successors = []
        original = self.state

        for i in range(5):
            for j in range(4):
                successor = copy.deepcopy(original)
                successor[i][j] = successor[i][j + 1]
                successor[i][j + 1] = original[i][j]
                successors.append(CheckersState(successor))

                successor = copy.deepcopy(original)
                successor[j][i] = successor[j + 1][i]
                successor[j + 1][i] = original[j][i]
                successors.append(CheckersState(successor))

        return successors

    def print_level(self):
        """ Pretty print the level list """
        rows = []
        for row in self.state:
            str_row = [str(el) if el > 9 else (' ' + str(el)) for el in row]
            rows.append(' '.join(str_row))

        print('\n'.join(rows) + '\n')

    def print_path(self):
        """ Print a complete solution path by recursively printing parents """
        if self.parent:
            self.parent.print_path()

        self.print_level()
