""" Worker thread for performing A* search outside of GUI thread """
from PyQt4.QtCore import QThread, QSize

from src.algorithms.puzzles.nonogram.nonogram_state import NonogramState


class SearchWorker(QThread):
    """ Inherit QThread for easy threading """

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.size = QSize(0, 0)
        self.stars = 0
        self.gui = None
        self.nonogram_search = None

    def run(self):
        """ Called when thread is started, perform search and set solution
         create a NonogramState node that can be set in the GUI
        """
        solution = self.nonogram_search.best_first_search()

        node = NonogramState(
            solution.state,
            None,
            solution.domains,
            solution.solution_length
        )

        self.gui.node = node

    def __del__(self):
        self.exiting = True
        self.wait()

    def search(self, gui, nonogram_search):
        """ Sets up gui and nonogram search, and proceeds to start itself """
        self.gui = gui
        self.nonogram_search = nonogram_search

        self.start()
