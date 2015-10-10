import math


class Ov3y(object):

    # https://github.com/ov3y/2048-AI/blob/master/js/ai.js
    @classmethod
    def evaluation_function(cls, state):

        empty_cells = sum([int(el == 0) for row in state.board for el in row])

        smooth_weight = 0.1
        mono2weight = 1.0
        empty_weight = 2.7
        max_weight = 1.0

        return (cls.smoothness(state) * smooth_weight +
                cls.monotonicity(state) * mono2weight +
                math.log(empty_cells + 1) * empty_weight +
                state.max_tile() * max_weight)

    @classmethod
    def monotonicity(cls, state):
        marked = []
        queued = []
        highest_value = 0
        highest_cell = (0, 0)

        for y in range(4):
            marked.append([])
            queued.append([])

            for x in range(4):
                marked[y].append(False)
                queued[y].append(False)

                if state.board[y][x] > highest_value:
                    highest_cell = (x, y)
                    highest_value = state.board[y][x]

        increases = 0
        cell_queue = [highest_cell]

        queued[highest_cell[1]][highest_cell[0]] = True

        mark_list = [highest_cell]

        mark_after = True

        while len(cell_queue) > 0:
            mark_after -= 1
            increases, mark_after = cls.mark_and_score(cell_queue.pop(0),
                                                       mark_list, marked,
                                                       queued, cell_queue,
                                                       mark_after, state)

        return -increases

    @classmethod
    def mark_and_score(cls, cell, mark_list, marked, queued, cell_queue,
                       mark_after, state):
        increases = 0
        mark_list.append(cell)

        if state.board[cell[1]][cell[0]] > 0:
            value = math.log(state.board[cell[1]][cell[0]]) / math.log(2)
        else:
            value = 0

        for direction in state.possible_moves.values():
            target = (cell[0] + direction[0], cell[1] + direction[1])

            if not (target[0] in range(4) and target[1] in range(4)):
                continue

            if not marked[target[1]][target[0]]:
                if state.board[target[1]][target[0]] > 0:
                    target_value = math.log(state.board[target[1]][target[0]]) / math.log(2)

                    if target_value > value:
                        increases += target_value - value

                if not queued[target[1]][target[0]]:
                    cell_queue.append(target)
                    queued[target[1]][target[0]] = True

        if mark_after == 0:
            while len(mark_list) > 0:
                cel = mark_list.pop()
                marked[cel[1]][cel[0]] = True

            mark_after = len(cell_queue)
        return increases, mark_after

    @classmethod
    def smoothness(cls, state):
        smoothness = 0
        for x in range(4):
            for y in range(4):
                if state.board[y][x] != 0:
                    value = math.log(state.board[y][x]) / math.log(2)
                    # TODO Fix usage of value, now unused

                    for direction in [(0, -1), (1, 0)]:
                        target = cls.find_farthest((x, y), direction, state)

                        if state.board[target[1]][target[0]] != 0:
                            value = state.board[target[1]][target[0]]
                            target_value = math.log(value) / math.log(2)

                            smoothness -= abs(value - target_value)
        return smoothness

    @classmethod
    def find_farthest(cls, cell, direction, state):
        while cell[0] in range(4) and cell[1] in range(4) and state.board[cell[1]][cell[0]] == 0:
            cell = (cell[0] + direction[0], cell[1] + direction[1])

        return cell
