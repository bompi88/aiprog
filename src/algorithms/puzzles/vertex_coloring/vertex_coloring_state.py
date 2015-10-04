""" Specialization of SearchState """
from collections import OrderedDict
from src.utils.domaincopy import domaincopy
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

        # Look at the solution domain, and use log to transform
        # it to simple additions in the solution space
        for domain in self.domains.values():
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

        viable_domains = {
            key: domain for key, domain in self.domains.items() if len(domain) > 1
        }

        sorted_domains = OrderedDict(sorted(viable_domains.items(), key=lambda x: -len(x[1])))

        (key, domain) = sorted_domains.popitem()

        for color in domain:
            new_domains = domaincopy(self.domains)
            new_domains[key] = [color]

            successor = VertexColoringState(self.state, self.gac, self.num_colors, new_domains, self._solution_length + 1, key, self.new_variable)
            result = self.gac.rerun(new_domains, key)

            if successor.is_solution():
                return [successor]

            if result:
                successors.append(successor)

        return successors

    def print_level(self):
        print '\nVC State'
        print [self.state.nv, self.state.ne]
        print self.state.vertices
        print self.state.edges
        print self.domains
