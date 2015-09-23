""" Specialization of SearchState """
from copy import deepcopy
from src.algorithms.astar.search_state import SearchState
from src.algorithms.gac.gac import GAC
from collections import OrderedDict
import itertools


class NonogramState(SearchState):
    """  """

    def __init__(self, graph, gac, domains=None, solution_length=0, new_variable=None, last_variable=None):
        if domains:
            self.domains = domains
        else:
            self.domains = OrderedDict()
            for i in range(len(graph.rows)):
                print graph.rows[i]

            for j in range(len(graph.columns)):
                print graph.columns[j]

        self.gac = gac
        self._solution_length = solution_length
        self.new_variable = new_variable
        self.last_variable = last_variable

        SearchState.__init__(self, graph)

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

        # viable_domains = {
        #     key: domain for key, domain in self.domains.items() if len(domain) > 1
        # }
        #
        # # foo = OrderedDict(sorted(foo.iteritems(), key=lambda x: x[1]['depth']))
        #
        # sorted_domains = OrderedDict(sorted(viable_domains.items(), key=lambda x: len(x[1])))
        #
        # for key, domain in sorted_domains.items():
        #     for color in domain:
        #         new_domain = deepcopy(self.domains)
        #         new_domain[key] = [color]
        #
        #         assumption = (key, [color])
        #
        #         successor = NonogramState(self.state, self.gac, new_domain, self._solution_length + 1, key, self.new_variable)
        #         self.gac.rerun(new_domain, assumption)
        #
        #         successors.append(successor)

        return successors

    def print_level(self):
        print '\nVC State'
        print [self.state.x, self.state.y]
        print self.state.rows
        print self.state.columns
        print self.domains
