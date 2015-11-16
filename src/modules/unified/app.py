""" Unified app for the entire course """
from PyQt4 import QtGui

from src.modules.module1.main_window import MainWindow as Navigation
from src.modules.module2.main_window import MainWindow as Graph
from src.modules.module3.main_window import MainWindow as Nonogram
from src.modules.module4.main_window import MainWindow as Play2048


class App(object):
    """ Loads a navigation window as default, and lets the user choose between
    all the different modules from the course """
    def __init__(self, qt_app):
        self.qt_app = qt_app
        self.main_window = Play2048()
        self.qt_app.setActiveWindow(self.main_window)

        self.add_switcher_menu()

    def loader(self, cls):
        self.main_window.close()
        self.main_window = cls()
        self.qt_app.setActiveWindow(self.main_window)

        self.add_switcher_menu()

    def navigation(self):
        """ Loads a Navigation instance into main window """
        self.loader(Navigation)

    def graph(self):
        """ Loads a Graph instance into main window """
        self.loader(Graph)

    def nonogram(self):
        """ Loads a Nonogram instance into main window """
        self.loader(Nonogram)

    def play_2048(self):
        """ Loads a Nonogram instance into main window """
        self.loader(Play2048)

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

        play_2048_action = QtGui.QAction('&2048', self.main_window)
        play_2048_action.triggered.connect(self.play_2048)

        menu = self.main_window.menuBar()
        module_menu = menu.addMenu('&Modules')
        module_menu.addAction(navigation_action)
        module_menu.addAction(graph_action)
        module_menu.addAction(nonogram_action)
        module_menu.addAction(play_2048_action)


def main():
    """ Creates Qt app and loads default level """
    import sys
    qt_app = QtGui.QApplication(sys.argv)
    _ = App(qt_app)
    sys.exit(qt_app.exec_())

if __name__ == '__main__':
    main()
