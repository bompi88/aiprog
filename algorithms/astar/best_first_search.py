__author__ = 'krisvage'

import time
import heapq as q
from search_state import SearchState

OPEN   = 0
CLOSED = 1
NEW    = 2

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
            if parent.g + self.arc_cost(parent, child) < child.g:
                child.parent = parent
                child.g      = parent.g + self.arc_cost(parent, child)
                child.f      = child.g + child.h
                self.propagate_path_improvements(child)

    def arc_cost(self, a, b):
        raise NotImplementedError('Implement arc_cost() in BestFirstSearch subclass')

    def create_root_node(self):
        raise NotImplementedError('Implement create_root_node() in BestFirstSearch subclass')

    def describe_solution(self, nodes, solution_length, t0):
        t1 = time.time()

        total = t1-t0

        print(str(nodes) + ' generated giving ' + str(solution_length) + ' as length, using ' + str(total) + ' seconds')

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

        t0 = time.time()

        while open:
            x = q.heappop(open)[1]

            closed.append(x)
            x.status = CLOSED

            if self.gui:
                self.gui.paint(x)
                time.sleep(200.0 / 1000)

            if x.is_solution():
                self.describe_solution(len(generated), x.solution_length(), t0)

                if self.gui:
                    self.gui.paint(x)
                return x

            succ = x.generate_all_successors(generated)

            for s in succ:
                if s.id in generated:
                    s = generated[s.id]

                x.add_child(s)

                if s.status is NEW:
                    self.attach_and_eval(s, x)
                    q.heappush(open, (s.f, s))
                    s.status = OPEN
                elif (x.g + self.arc_cost(x, s)) < s.g:
                    self.attach_and_eval(s, x)
                    if s.status is CLOSED:
                        self.propagate_path_improvements(s)
