""" Worker thread for performing A* search outside of GUI thread """
from PyQt4.QtCore import QThread, QSize

from src.algorithms.puzzles.navigation.navigation_grid import NavigationGrid
from src.algorithms.puzzles.navigation.navigation_state import NavigationState


class SearchWorker(QThread):
    """ Implement QThread for easy threading """

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.size = QSize(0, 0)
        self.stars = 0
        self.gui = None
        self.navigation = None

    def run(self):
        """ Called when thread is started, perform search and set solution
         create a NavigationState node that can be set in the GUI
        """
        solution = self.navigation.best_first_search()

        visited = solution.state.visited_copy()

        node = NavigationState(NavigationGrid(
            self.gui.node.state.map,
            visited,
            solution.state.current_pos
        ))

        self.gui.node = node

    def __del__(self):
        self.gui.status_message.emit(str('Killing search'))
        self.exiting = True
        self.wait()

    def search(self, gui, navigation):
        """ Sets up gui and navigation, and proceeds to start itself """
        self.gui = gui
        self.navigation = navigation

        self.start()
