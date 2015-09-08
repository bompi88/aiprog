__author__ = 'krisvage'

import time
import heapq as q
from search_state import SearchState

CLOSED = 1

class BestFirstSearch:
    def __init__(self, start, gui=None):
        self.start = start
        self.gui   = gui

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

    def describe_solution(self, nodes, solution_length):
        print(str(nodes) + ' generated giving ' + str(solution_length) + ' as length')

    def best_first_search(self):
        closed = []
        open   = []

        generated = {}

        n0 = self.create_root_node()

        n0.g = 0
        n0.h = n0.heuristic_evaluation()
        n0.f = n0.g + n0.h

        generated[n0.id] = n0

        q.heappush(open, (n0.f, n0))

        while open:
            x = q.heappop(open)[1]

            closed.append(x)
            x.status = CLOSED

            if self.gui:
                self.gui.paint(x)
                time.sleep(200.0 / 1000)

            if x.is_solution():
                self.describe_solution(len(generated), x.solution_length())

                if self.gui:
                    self.gui.paint(x)
                return x

            succ = x.generate_all_successors(generated)

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