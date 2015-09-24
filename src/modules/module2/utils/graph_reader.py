""" Represent a graph """
import os
import res
from PyQt4 import QtGui


class GraphReader(object):
    # pylint: disable=too-many-instance-attributes

    def __init__(self, graph):
        self.nv, self.ne, self.vertices, self.edges = graph

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

    def init_constraints_and_variables(self):
        for edge in self.edges:
            for v in edge:
                self.variables.add('v' + str(v))

            self.constraints.append('v{} != v{}'.format(edge[0], edge[1]))

    @staticmethod
    def load_level(gui):
        """ Load level with a QFileDialog """
        if gui.graph is None:
            filename = 'graph-color-1.txt'
        else:
            path = QtGui.QFileDialog.getOpenFileName(
                gui.window(), "Open Map File", "", "Text files (*.txt)"
            )
            filename = list(path.split('/')).pop()

        if not filename:
            return

        return [
            filename,
            GraphReader(
                GraphReader.parse_graph(GraphReader.read_graph(filename))
            )
        ]

    @staticmethod
    def parse_graph(lines):
        nv, ne = [int(s) for s in lines.pop(0).split(' ')]

        vertices = [[s for s in lines.pop(0).split(' ')] for _ in range(nv)]

        for i, vertex in enumerate(vertices):
            vertices[i] = [int(vertex[0]), float(vertex[1]), float(vertex[2])]

        edges = [[int(s) for s in lines.pop(0).split(' ')] for _ in range(ne)]

        return [nv, ne, vertices, edges]

    @staticmethod
    def read_graph(filename):
        """ Read a file from /maps """
        path = os.path.dirname(res.__file__)
        path += '/graphs/' + filename
        graph_file = open(path, 'r')
        contents = graph_file.read()
        return contents.splitlines()

g = GraphReader(GraphReader.parse_graph(GraphReader.read_graph('graph-color-1.txt')))
print g.constraints
print g.variables
