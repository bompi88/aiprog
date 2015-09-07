__author__ = 'krisvage'

import heapq as q
from search_state import SearchState

CLOSED = 1

class BestFirstSearch:
    def __init__(self, start):
        self.start = start

    def attach_and_eval(self, child, parent):
        child.parent = parent
        child.g      = parent.g + self.arc_cost(parent, child)
        child.h      = child.heuristic_evaluation()
        child.f      = child.g + child.h

    def propagate_path_improvements(self, parent):
        for child in parent.kids:
            if parent.g  + self.arc_cost(parent, child) < child.g:
                child.parent = parent
                child.g      = parent.g + self.arc_cost(parent, child)
                child.f      = child.g + child.h
                self.propagate_path_improvements(child)

    def arc_cost(self, a, b):
        raise NotImplementedError('Implement arc_cost() in BestFirstSearch subclass')

    def create_root_node(self):
        raise NotImplementedError('Implement create_root_node() in BestFirstSearch subclass')

    def best_first_search(self):
        closed = []
        open   = []

        generated = {}

        n0 = self.create_root_node()

        n0.g = 0
        n0.h = n0.heuristic_evaluation()
        n0.f = n0.g + n0.h

        q.heappush(open, (n0.f, n0))

        tmp = 1
        succs = 0

        while True:
            if len(open) == 0:
                return -1

            x = q.heappop(open)[1]

            closed.append(x)
            x.status = CLOSED

            print(str(tmp) + ': succs - ' + str(succs) + ' - ' + x.id)
            tmp += 1

            if x.is_solution():
                return x

            succ = x.generate_all_successors(generated)

            succs += len(succ)

            for s in succ:
                if s.id in generated:
                    s = generated[s.id]

                x.add_child(s)

                if (not (s.f, s) in open) and (not s in closed):
                    self.attach_and_eval(s, x)
                    q.heappush(open, (s.f, s))
                elif (x.g + self.arc_cost(x, s)) < s.g:
                    self.attach_and_eval(s, x)
                    if s in closed:
                        self.propagate_path_improvements(s)
