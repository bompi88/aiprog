"""
    # https://github.com/ov3y/2048-AI/blob/master/js/ai.js
    def evaluation_function(self):
        empty_cells = sum([int(el == 0) for row in self.board for el in row])

        smooth_weight = 0.1
        mono2weight = 1.0
        empty_weight = 2.7
        max_weight = 1.0

        return (self.smoothness() * smooth_weight +
                self.monotonicity() * mono2weight +
                math.log(empty_cells) * empty_weight +
                self.max_tile() * max_weight)

    def monotonicity(self):
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

                if self.board[y][x] > highest_value:
                    highest_cell = (x, y)
                    highest_value = self.board[y][x]

        increases = 0
        cell_queue = [highest_cell]

        queued[highest_cell[1]][highest_cell[0]] = True

        mark_list = [highest_cell]

        mark_after = True

        ##

        while len(cell_queue) > 0:
            mark_after -= 1
            increases, mark_after = self.mark_and_score(cell_queue.pop(0), mark_list, marked, queued, cell_queue, mark_after)

        return -increases

    def mark_and_score(self, cell, mark_list, marked, queued, cell_queue, mark_after):
        increases = 0
        mark_list.append(cell)

        if self.board[cell[1]][cell[0]] > 0:
            value = math.log(self.board[cell[1]][cell[0]]) / math.log(2)
        else:
            value = 0

        for direction in self.possible_moves.values():
            target = (cell[0] + direction[0], cell[1] + direction[1])

            if target[0] in range(4) and target[1] in range(4) and not marked[target[1]][target[0]]:
                if self.board[target[1]][target[0]] > 0:
                    target_value = math.log(self.board[target[1]][target[0]])

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


    def smoothness(self):
        smoothness = 0
        for x in range(4):
            for y in range(4):
                if self.board[y][x] != 0:
                    value = math.log(self.board[y][x]) / math.log(2)
                    for direction in [(0, -1), (1, 0)]:
                        target = self.find_farthest((x, y), direction)

                        if self.board[target[1]][target[0]] != 0:
                            value = self.board[target[1]][target[0]]
                            target_value = math.log(value) / math.log(2)

                            smoothness -= abs(value - target_value)
        return smoothness

    def find_farthest(self, cell, direction):
        while cell[0] in range(4) and cell[1] in range(4) and self.board[cell[1]][cell[0]] == 0:
            cell = (cell[0] + direction[0], cell[1] + direction[1])

        return cell
"""
