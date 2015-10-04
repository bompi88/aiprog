if self.diagonal:
  viable_movements = [[-1, -1], [1, 1], [1, -1], [-1, 1],
                     [-1, 0], [1, 0], [0, -1], [0, 1]]
else:
  viable_movements = [[-1, 0], [1, 0], [0, -1], [0, 1]]