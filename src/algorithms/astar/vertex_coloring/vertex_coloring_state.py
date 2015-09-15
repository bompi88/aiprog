""" Specialization of SearchState """
from copy import deepcopy
from src.algorithms.astar.search_state import SearchState
from src.algorithms.astar.vertex_coloring.utils.const import C
from src.algorithms.gac.gac import GAC
from collections import OrderedDict


class VertexColoringState(SearchState):
    """  """

    def __init__(self, graph, gac, domains=None, solution_length=0):
        if domains:
            self.domains = domains
        else:
            self.domains = OrderedDict()
            for i in range(graph.nv):
                self.domains['v' + str(i)] = [C.RED, C.GREEN, C.BLUE, C.ORANGE]

        self.gac = gac
        self._solution_length = solution_length

        SearchState.__init__(self, graph)

    def create_state_identifier(self):
        # return ':'.join([str(len(domain) == 1) for domain in self.domains.values()])
        return ':'.join([','.join(str(d) for d in domain) for domain in self.domains.values()])

    def heuristic_evaluation(self):
        sum_h = 0

        for domain in self.domains.values():
            if (len(domain) == 1):
                sum_h -= 0.05
            elif (len(domain) == 0):
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

        print(viable_domains)

        # foo = OrderedDict(sorted(foo.iteritems(), key=lambda x: x[1]['depth']))

        sorted_domains = OrderedDict(sorted(viable_domains.items(), key=lambda x: len(x[1])))

        print(sorted_domains)

        for key, domain in sorted_domains.items():
            for color in domain:
                new_domain = deepcopy(self.domains)
                new_domain[key] = [color]

                assumption = (key, [color])

                successor = VertexColoringState(self.state, self.gac, new_domain, self._solution_length + 1)
                self.gac.rerun(new_domain, assumption)

                successors.append(successor)

        return successors

    def print_level(self):
        print '\nVC State'
        print [self.state.nv, self.state.ne]
        print self.state.vertices
        print self.state.edges
        print self.domains
