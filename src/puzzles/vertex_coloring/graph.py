""" Represent a graph """
from src.puzzles.vertex_coloring.vertex_constraint import VertexConstraint


class Graph(object):
    # pylint: disable=too-many-instance-attributes

    def __init__(self, lines):
        self.nv, self.ne, self.vertices, self.edges = self.parse(lines)

        min_x = min([vertex[1] for vertex in self.vertices])
        max_x = max([vertex[1] for vertex in self.vertices])
        min_y = min([vertex[2] for vertex in self.vertices])
        max_y = max([vertex[2] for vertex in self.vertices])

        self.min_x = self.min_y = min(min_x, min_y)
        self.max_x = self.max_y = max(max_x, max_y)

        self.width = self.max_x - self.min_x
        self.height = self.max_y - self.min_y

        self.constraints = []
        self.variables = set([])
        self.init_constraints_and_variables()

    def parse(self, lines):
        nv, ne = [int(s) for s in lines.pop(0).split(' ')]

        vertices = [[s for s in lines.pop(0).split(' ')] for _ in range(nv)]

        for i, vertex in enumerate(vertices):
            vertices[i] = [int(vertex[0]), float(vertex[1]), float(vertex[2])]

        edges = [[int(s) for s in lines.pop(0).split(' ')] for _ in range(ne)]

        return [nv, ne, vertices, edges]

    def init_constraints_and_variables(self):
        for v in range(self.nv):
            self.variables.add('v' + str(v))

        for edge in self.edges:
            self.constraints.append(
                VertexConstraint('v{} != v{}'.format(edge[0], edge[1]))
            )
