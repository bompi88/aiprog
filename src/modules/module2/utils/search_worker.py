""" Worker thread for performing A* search outside of GUI thread """
from PyQt4.QtCore import QThread, QSize

from src.algorithms.puzzles.vertex_coloring.vertex_coloring_state import VertexColoringState


class SearchWorker(QThread):
    """ Inherit QThread for easy threading """

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.size = QSize(0, 0)
        self.stars = 0
        self.gui = None
        self.vertex_search = None

    def run(self):
        """ Called when thread is started, perform search and set solution
         create a VertexColoringState node that can be set in the GUI
        """
        solution = self.vertex_search.best_first_search()

        node = VertexColoringState(
            solution.state,
            None,
            solution.domains,
            solution.solution_length
        )

        self.gui.node = node

    def __del__(self):
        self.exiting = True
        self.wait()

    def search(self, gui, vertex_search):
        """ Sets up gui and vertex search, and proceeds to start itself """
        self.gui = gui
        self.vertex_search = vertex_search

        self.start()
