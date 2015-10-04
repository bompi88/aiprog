""" Specialization of SearchState """
from src.algorithms.astar.search_state import SearchState
import math
from src.utils.domaincopy import domaincopy
from collections import OrderedDict


class NonogramState(SearchState):
    """  """
    def __init__(self, nonogram, gac, domains=None, solution_length=0):
        if domains:
            self.domains = domains
        else:
            self.domains = {}
            for k in range(nonogram.y):
                self.domains['r' + str(nonogram.y - k - 1)] = NonogramState.init_domain(
                    nonogram.x, nonogram.rows[k]
                )

            for l in range(nonogram.x):
                self.domains['c' + str(l)] = NonogramState.init_domain(
                    nonogram.y, nonogram.columns[l]
                )

        self.gac = gac
        self._solution_length = solution_length
        self.state = nonogram

        SearchState.__init__(self, nonogram)

    @staticmethod
    def init_domain(length, blocks, domains=None, total_length=None):
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
                d = domains[i] + part_domain
                if len(d) < total_length + 2:
                    new_domains.append(d)

        return NonogramState.init_domain(length - first, rest, new_domains, total_length)

    def create_state_identifier(self):
        return ':'.join([','.join(str(d) for d in domain) for domain in self.domains.values()])

    def heuristic_evaluation(self):
        sum_h = 0

        for domain in self.domains.values():
            if len(domain) == 0:
                sum_h += 1000
            else:
                sum_h += math.log(len(domain))

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
            key: domain for key, domain in self.domains.items() if len(domain) > 1
        }

        sorted_domains = OrderedDict(sorted(viable_domains.items(), key=lambda x: -len(x[1])))

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

    def print_level(self):
        print '\nNonogram State'
        print [self.state.x, self.state.y]
        print self.state.rows
        print self.state.columns
        print self.domains
