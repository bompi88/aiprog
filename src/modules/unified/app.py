""" Unified app for the entire course """
from PyQt4 import QtGui

from src.modules.module1.main_window import MainWindow as Navigation
from src.modules.module2.main_window import MainWindow as Graph
from src.modules.module3.main_window import MainWindow as Nonogram


class App(object):
    """ Loads a navigation window as default, and lets the user choose between
    all the different modules from the course """
    def __init__(self, qt_app):
        self.qt_app = qt_app
        self.main_window = Navigation()
        self.qt_app.setActiveWindow(self.main_window)

        self.add_switcher_menu()

    def navigation(self):
        """ Loads a Navigation instance into main window """
        self.main_window.close()
        self.main_window = Navigation()
        self.qt_app.setActiveWindow(self.main_window)

        self.add_switcher_menu()

    def graph(self):
        """ Loads a Graph instance into main window """
        self.main_window.close()
        self.main_window = Graph()
        self.qt_app.setActiveWindow(self.main_window)

        self.add_switcher_menu()

    def nonogram(self):
        """ Loads a Nonogram instance into main window """
        self.main_window.close()
        self.main_window = Nonogram()
        self.qt_app.setActiveWindow(self.main_window)

        self.add_switcher_menu()

    def add_switcher_menu(self):
        """ Adds the following items to the menubar:
         Modules -> [ Navigation, Graphs, Nonograms ]
        """
        navigation_action = QtGui.QAction('&Navigation', self.main_window)
        navigation_action.triggered.connect(self.navigation)

        graph_action = QtGui.QAction('&Graphs', self.main_window)
        graph_action.triggered.connect(self.graph)

        nonogram_action = QtGui.QAction('&Nonograms', self.main_window)
        nonogram_action.triggered.connect(self.nonogram)

        menu = self.main_window.menuBar()
        file_menu = menu.addMenu('&Modules')
        file_menu.addAction(navigation_action)
        file_menu.addAction(graph_action)
        file_menu.addAction(nonogram_action)


def main():
    """ Creates Qt app and loads default level """
    import sys
    qt_app = QtGui.QApplication(sys.argv)
    _ = App(qt_app)
    sys.exit(qt_app.exec_())

if __name__ == '__main__':
    main()
