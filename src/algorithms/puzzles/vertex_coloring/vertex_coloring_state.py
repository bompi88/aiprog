""" Specialization of SearchState """
from src.utils.domaincopy import domaincopy
from collections import OrderedDict
import itertools
import math

from src.algorithms.astar.search_state import SearchState
from src.algorithms.puzzles.vertex_coloring.utils.const import C


class VertexColoringState(SearchState):
    """  """

    def __init__(self, graph, gac, num_colors, domains=None, solution_length=0, new_variable=None, last_variable=None):

        viable_values = [C.RED, C.GREEN, C.BLUE, C.ORANGE, C.PINK, C.YELLOW, C.PURPLE, C.BROWN]

        if domains:
            self.domains = domains
        else:
            self.domains = OrderedDict()
            for i in range(graph.nv):
                self.domains['v' + str(i)] = viable_values[:num_colors]

        self.gac = gac
        self._solution_length = solution_length
        self.new_variable = new_variable
        self.last_variable = last_variable
        self.num_colors = num_colors

        SearchState.__init__(self, graph)

    def create_state_identifier(self):
        # return ':'.join([str(len(domain) == 1) for domain in self.domains.values()])
        return ':'.join([','.join(str(d) for d in domain) for domain in self.domains.values()])

    def heuristic_evaluation(self):
        sum_h = 0

        # Give penalty for not being a neighbor
        if self.last_variable:
            variables_tbc_old = set(itertools.chain(*[self.gac.constraint_map[x] for x in self.gac.variable_map[self.last_variable]]))

            if self.new_variable not in variables_tbc_old:
                sum_h += math.log(10)

        # Give credits for being the most constrained vertex
        if self.new_variable:
            variables_tbc_new = set(itertools.chain(*[self.gac.constraint_map[x] for x in self.gac.variable_map[self.new_variable]]))
            sum_h -= math.log(len(variables_tbc_new) * 20)

        # Look at the solotion domain, and use log to transform
        # it to simple additions in the solution space
        for domain in self.domains.values():
            if len(domain) == 0:
                sum_h += math.log(10)
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

    def vertex_color(self, sid):
        domain = self.domains['v' + str(sid)]

        if len(domain) > 1:
            return C.WHITE
        elif len(domain) == 1:
            return domain[0]
        else:
            return C.BLACK

    def generate_all_successors(self):
        successors = []

        # TODO Guess the smartest child

        viable_domains = {
            key: domain for key, domain in self.domains.items() if len(domain) > 1
        }

        # foo = OrderedDict(sorted(foo.iteritems(), key=lambda x: x[1]['depth']))

        sorted_domains = OrderedDict(sorted(viable_domains.items(), key=lambda x: len(x[1])))

        for key, domain in sorted_domains.items():
            for color in domain:

                new_domain = domaincopy(self.domains)
                new_domain[key] = [color]

                assumption = (key, [color])

                successor = VertexColoringState(self.state, self.gac, self.num_colors, new_domain, self._solution_length + 1, key, self.new_variable)
                self.gac.rerun(new_domain, assumption)

                successors.append(successor)

        return successors

    def print_level(self):
        print '\nVC State'
        print [self.state.nv, self.state.ne]
        print self.state.vertices
        print self.state.edges
        print self.domains
