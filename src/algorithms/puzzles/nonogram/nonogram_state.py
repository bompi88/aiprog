""" Specialization of SearchState """
from copy import deepcopy
from src.algorithms.astar.search_state import SearchState
from collections import OrderedDict


class NonogramState(SearchState):
    """  """

    def __init__(self, nonogram, gac, domains=None, solution_length=0, new_variable=None, last_variable=None):
        if domains:
            self.domains = domains
        else:
            self.domains = OrderedDict()
            for k in range(len(nonogram.rows)):
                self.domains['r' + str(k)] = NonogramState.init_domain(
                    nonogram.x, nonogram.rows[k]
                )

            for l in range(len(nonogram.columns)):
                self.domains['c' + str(l)] = NonogramState.init_domain(
                    nonogram.y, nonogram.columns[l]
                )

        self.gac = gac
        self._solution_length = solution_length
        self.new_variable = new_variable
        self.last_variable = last_variable
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

        if rest:
            min_length_rest = sum(rest) + len(rest)
        else:
            min_length_rest = 0

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
            if len(domain) == 1:
                sum_h -= 0.05
            elif len(domain) == 0:
                sum_h += 5
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

        # TODO create successors

        viable_domains = {
            key: domain for key, domain in self.domains.items() if len(domain) > 1
        }

        sorted_domains = OrderedDict(sorted(viable_domains.items(), key=lambda x: len(x[1])))

        for key, domain in sorted_domains.items():
            for element in domain:
                new_domain = deepcopy(self.domains)
                new_domain[key] = [element]

                assumption = (key, [element])

                successor = NonogramState(self.state, self.gac, new_domain, self._solution_length + 1, key, self.new_variable)
                self.gac.rerun(new_domain, assumption)

                successors.append(successor)

        return successors

    def print_level(self):
        print '\nNonogram State'
        print [self.state.x, self.state.y]
        print self.state.rows
        print self.state.columns
        print self.domains
