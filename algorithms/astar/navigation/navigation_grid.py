class NavigationGrid:
    def __init__(self, map, grid=[], visited = []):
        self.map         = map
        self.grid        = grid or map.grid
        self.visited     = visited or map.visited
        self.current_pos = map.current_pos

    def goal(self):
        return self.map.goal

    def x_dim(self):
        return self.map.x_dim()

    def y_dim(self):
        return self.map.y_dim()


