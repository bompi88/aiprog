""" Specialization of SearchState """
from copy import deepcopy
from src.algorithms.astar.search_state import SearchState
from src.algorithms.astar.vertex_coloring.utils.const import C
from src.algorithms.gac.gac import GAC


class VertexColoringState(SearchState):
    """  """

    def __init__(self, graph, domains=None):
        self.domains = domains or [
            [C.RED, C.GREEN, C.BLUE, C.ORANGE] for _ in range(graph.nv)
        ]

        SearchState.__init__(self, graph)

    def create_state_identifier(self):
        return ':'.join([','.join(str(d) for d in domain) for domain in self.domains])

    def heuristic_evaluation(self):
        sum_h = 0

        for domain in self.domains:
            length = len(domain) - 1
            sum_h += length

        return sum_h

    def is_solution(self):
        for domain in self.domains:
            if len(domain) > 1:
                return False

        return True

    def solution_length(self):
        return 1

    def vertex_color(self, sid):
        domain = self.domains[sid]

        if len(domain) > 1:
            return C.WHITE
        else:
            return domain[0]

    def generate_all_successors(self):
        successors = []

        for i, domain in enumerate(self.domains):
            if len(domain) > 1:
                for color in domain:
                    new_domain = deepcopy(self.domains)
                    new_domain[i] = [color]

                    successor = VertexColoringState(self.state, new_domain)
                    gac = GAC(successor) # TODO fix
                    # gac.rerun()
                    successors.append(successor)

        return successors

    def print_level(self):
        print '\nVC State'
        print [self.state.nv, self.state.ne]
        print self.state.vertices
        print self.state.edges
        print self.domains
