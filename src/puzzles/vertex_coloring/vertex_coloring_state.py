""" Specialization of SearchState """
from collections import OrderedDict
import math

from src.utils.domaincopy import domaincopy
from src.algorithms.astar.search_state import SearchState
from src.utils.const import C


class VertexColoringState(SearchState):
    """ State of a vertex coloring search """

    def __init__(self, graph, gac, num_colors, domains=None, solution_length=0):
        # pylint: disable=too-many-arguments

        viable_values = [
            C.graph_colors.RED, C.graph_colors.GREEN, C.graph_colors.BLUE,
            C.graph_colors.ORANGE, C.graph_colors.PINK, C.graph_colors.YELLOW,
            C.graph_colors.PURPLE, C.graph_colors.BROWN, C.graph_colors.CYAN,
            C.graph_colors.DARK_BROWN
        ]

        if domains:
            self.domains = domains
        else:
            self.domains = OrderedDict()
            for i in range(graph.nv):
                self.domains['v' + str(i)] = viable_values[:num_colors]

        self.gac = gac
        self._solution_length = solution_length
        self.num_colors = num_colors

        SearchState.__init__(self, graph)

    def create_state_identifier(self):
        return ':'.join([','.join(str(d) for d in domain)
                         for domain in self.domains.values()])

    def heuristic_evaluation(self):
        # Look at the solution domain, and use log to transform
        # it to simple additions in the solution space
        return sum([math.log(len(domain)) for domain in self.domains.values()])

    def is_solution(self):
        return self.h == 0

    def solution_length(self):
        return self._solution_length

    def vertex_color(self, sid):
        """ Returns the color of vertex. Either the correct color, white
        if there are still several valid domains, and black if the domain
        list has become empty. Black should be treated as an error. """
        domain = self.domains['v' + str(sid)]

        if len(domain) > 1:
            return C.graph_colors.WHITE
        elif len(domain) == 1:
            return domain[0]
        else:
            return C.graph_colors.BLACK

    def generate_all_successors(self):
        successors = []

        viable_domains = {
            k: domain for k, domain in self.domains.items() if len(domain) > 1
        }

        sorted_domains = OrderedDict(
            sorted(viable_domains.items(), key=lambda x: -len(x[1]))
        )

        (key, domain) = sorted_domains.popitem()

        for color in domain:
            new_domains = domaincopy(self.domains)
            new_domains[key] = [color]

            successor = VertexColoringState(
                self.state, self.gac, self.num_colors, new_domains,
                self._solution_length + 1
            )
            result = self.gac.rerun(new_domains, key)

            if successor.is_solution():
                return [successor]

            if result:
                successors.append(successor)

        return successors

    def print_level(self):
        """ Prints a state to the terminal, for aid in debugging. """
        print '\nVC State'
        print [self.state.nv, self.state.ne]
        print self.state.vertices
        print self.state.edges
        print self.domains
