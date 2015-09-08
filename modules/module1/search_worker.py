__author__ = 'krisvage'

from PyQt4.QtCore import QThread, QSize

from algorithms.astar.navigation.navigation_state import NavigationGrid


class SearchWorker(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.size = QSize(0, 0)
        self.stars = 0

    def run(self):
        solution = self.navigation.best_first_search()

        visited = solution.state.visited
        board   = self.gui.board

        node = NavigationGrid(
            self.gui.node.map,
            board,
            visited
        )

        self.gui.node = node

    def __del__(self):
        self.exiting = True
        self.wait()

    def search(self, gui, navigation):
        self.gui = gui
        self.navigation = navigation

        self.start()
