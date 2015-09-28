""" A GUI application for showing vertex coloring on graphs """
import os
import sys

from PyQt4 import QtGui

import res
from src.modules.module2.utils.graph_reader import GraphReader
from src.modules.module2.graph_gui import GraphGUI


class MainWindow(QtGui.QMainWindow):
    """ The GUI window which contains the Widgets and buttons """

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.graph_gui = GraphGUI(self)

        self.init_ui()

    def init_ui(self):
        """ Initializes the UI, delegates to init_menubar and init_toolbar """
        self.setCentralWidget(self.graph_gui)

        self.init_menubar()
        self.init_toolbar()

        status_bar = self.statusBar()
        self.graph_gui.status_message[str].connect(
            status_bar.showMessage
        )

        self.center()
        self.show()
        self.raise_()

    def init_menubar(self):
        """ Initializes a menubar with the following items:
         File -> [ Load, Kill, Exit ]
         Vertex Numbers -> [Yes, No]
        """
        load_action = QtGui.QAction('&Load graph', self)
        load_action.setShortcut('Ctrl+L')
        load_action.triggered.connect(
            lambda: self.graph_gui.set_graph(
                GraphReader.load_level(self.graph_gui)
            )
        )

        kill_action = QtGui.QAction('&Kill search', self)
        kill_action.setShortcut('Ctrl+K')
        kill_action.triggered.connect(self.graph_gui.thread.end_search)

        exit_action = QtGui.QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(QtGui.qApp.quit)

        yes_action = QtGui.QAction('&Yes', self)
        yes_action.triggered.connect(
            lambda: (self.graph_gui.set_vertex_numbering(True)
                     and self.numbering_changed(True))
        )

        no_action = QtGui.QAction('&No', self)
        no_action.triggered.connect(
            lambda: (self.graph_gui.set_vertex_numbering(False)
                     and self.numbering_changed(False))
        )

        menu = self.menuBar()
        menu.setNativeMenuBar(False)
        file_menu = menu.addMenu('&File')
        file_menu.addAction(load_action)
        file_menu.addAction(kill_action)
        file_menu.addAction(exit_action)

        numbering_menu = menu.addMenu('&Vertex Numbers')
        numbering_menu.addAction(yes_action)
        numbering_menu.addAction(no_action)

    def init_toolbar(self):
        """ Initializes a toolbar, with a run button and delay controls """
        path = os.path.dirname(res.__file__)
        path += '/imgs/'
        run_action = QtGui.QAction(QtGui.QIcon(path + 'play.png'), 'Run A*', self)
        run_action.setShortcut('Ctrl+R')
        run_action.setStatusTip('Run A*')
        run_action.triggered.connect(self.graph_gui.start_search)

        color_action_3 = QtGui.QAction('Colors 3', self)
        color_action_3.triggered.connect(
            lambda: self.graph_gui.set_color(3) and self.color_changed(3)
        )

        color_action_4 = QtGui.QAction('Colors 4', self)
        color_action_4.triggered.connect(
            lambda: self.graph_gui.set_color(4) and self.color_changed(4)
        )

        color_action_5 = QtGui.QAction('Colors 5', self)
        color_action_5.triggered.connect(
            lambda: self.graph_gui.set_color(5) and self.color_changed(5)
        )

        color_action_6 = QtGui.QAction('Colors 6', self)
        color_action_6.triggered.connect(
            lambda: self.graph_gui.set_color(6) and self.color_changed(6)
        )

        color_action_7 = QtGui.QAction('Colors 7', self)
        color_action_7.triggered.connect(
            lambda: self.graph_gui.set_color(7) and self.color_changed(7)
        )

        color_action_8 = QtGui.QAction('Colors 8', self)
        color_action_8.triggered.connect(
            lambda: self.graph_gui.set_color(8) and self.color_changed(8)
        )

        toolbar = self.addToolBar('Run')
        toolbar.addAction(run_action)
        toolbar.addAction(color_action_3)
        toolbar.addAction(color_action_4)
        toolbar.addAction(color_action_5)
        toolbar.addAction(color_action_6)
        toolbar.addAction(color_action_7)
        toolbar.addAction(color_action_8)

    def center(self):
        """ Center window  [http://zetcode.com/gui/pyqt4/firstprograms/] """
        geometry = self.frameGeometry()
        desktop_center = QtGui.QDesktopWidget().availableGeometry().center()
        geometry.moveCenter(desktop_center)
        self.move(geometry.topLeft())

    def color_changed(self, color):
        """ Writes to status bar when color is changed """
        self.statusBar().showMessage('Amount of colors available: ' + str(color))

    def numbering_changed(self, numbering):
        if numbering:
            self.statusBar().showMessage('Showing vertex numbers')
        else:
            self.statusBar().showMessage('Hiding vertex numbers')



def main():
    """ Creates Qt app and loads default level """
    app = QtGui.QApplication(sys.argv)

    main_window = MainWindow()
    filename, graph = list(GraphReader.load_level(main_window.graph_gui))
    main_window.graph_gui.level_loaded(filename, graph)
    main_window.graph_gui.update()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
