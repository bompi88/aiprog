""" Specialization of SearchState """
from src.algorithms.astar.search_state import SearchState

from src.utils.domaincopy import domaincopy
from collections import OrderedDict


class NonogramState(SearchState):
    """ A search state for a nonogram """
    def __init__(self, nonogram, gac, domains=None, solution_length=0):
        if domains:
            self.domains = domains
        else:
            self.domains = {}
            for row in range(nonogram.y):
                row_id = nonogram.y - row - 1
                self.domains['r' + str(row_id)] = NonogramState.init_domain(
                    nonogram.x, nonogram.rows[row]
                )

            for col in range(nonogram.x):
                self.domains['c' + str(col)] = NonogramState.init_domain(
                    nonogram.y, nonogram.columns[col]
                )

        self.gac = gac
        self._solution_length = solution_length

        SearchState.__init__(self, nonogram)

    @staticmethod
    def init_domain(length, blocks, domains=None, total_length=None):
        """ Helper method for creating all the possible domains of a given row
        or column. Example (5, [1 2]) => ['10110', '01011', '10011'] """
        if not total_length:
            total_length = length

        if not blocks:
            for i, domain in enumerate(domains):
                if len(domain) < total_length:
                    domains[i] = domain + ('0' * (total_length - len(domain)))
                elif len(domain) > total_length:
                    domains[i] = domain[0:total_length]

            return domains

        first, rest = blocks[0], blocks[1:]

        min_length_rest = sum(rest) + len(rest)

        free_space = length - min_length_rest
        max_index = free_space - first + 1

        if not domains:
            domains = ['']
        new_domains = []

        for i in range(0, max_index):
            part_domain = ('0' * i) + ('1' * first) + '0'

            for i in range(len(domains)):
                domain = domains[i] + part_domain
                if len(domain) < total_length + 2:
                    new_domains.append(domain)

        return NonogramState.init_domain(
            length - first, rest, new_domains, total_length
        )

    def create_state_identifier(self):
        state = self.representation()
        return ':'.join([','.join(str(e) for e in row) for row in state])

    def heuristic_evaluation(self):
        sum_h = 0

        for domain in self.domains.values():
            if len(domain) == 0:
                sum_h += 1000
            else:
                sum_h += len(domain) - 1

        return sum_h

    def is_solution(self):
        for domain in self.domains.values():
            if len(domain) != 1:
                return False

        return True

    def solution_length(self):
        return self._solution_length

    def generate_all_successors(self):
        successors = []

        viable_domains = {
            k: domain for k, domain in self.domains.items() if len(domain) > 1
        }

        sorted_domains = OrderedDict(
            sorted(viable_domains.items(), key=lambda x: -len(x[1])))

        (key, domain) = sorted_domains.popitem()

        for element in domain:
            new_domains = domaincopy(self.domains)
            new_domains[key] = [element]

            successor = NonogramState(self.state,
                                      self.gac,
                                      new_domains,
                                      self._solution_length + 1)
            result = self.gac.rerun(new_domains, key)

            if successor.is_solution():
                return [successor]

            if result:
                successors.append(successor)

        return successors

    def representation(self):
        """ Returns the state as printable 2D board """
        unset = 2
        empty_domain = 3
        state = [[unset] * self.state.x for _ in range(self.state.y)]

        for row in range(self.state.y):
            row_domains = self.domains['r' + str(row)]
            if len(row_domains) == 1:
                for i, element in enumerate(list(row_domains[0])):
                    state[row][i] = int(element)
            elif len(row_domains) == 0:
                for i in range(self.state.x):
                    state[row][i] = empty_domain

        for col in range(self.state.x):
            column_domains = self.domains['c' + str(col)]
            if len(column_domains) == 1:
                for i, element in enumerate(list(column_domains[0])):
                    state[i][col] = int(element)
            elif len(column_domains) == 0:
                for i in range(self.state.y):
                    state[i][col] = empty_domain

        return state

    def __str__(self):
        state = self.representation()

        return '\n'.join([' '.join([str(el) for el in col]) for col in state])

    def print_level(self):
        """ Prints state to terminal """
        print self
