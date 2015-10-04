""" A GUI application for showing vertex coloring on graphs """
from PyQt4 import QtGui

import res.imgs
from src.modules.module2.graph_gui import GraphGUI
from src.utils.func import make_function


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

        self.show()
        self.raise_()

    def init_menubar(self):
        """ Initializes a menubar with the following items:
         File -> [ Load, Kill, Exit ]
         Vertex Numbers -> [Yes, No]
         Delay -> [0 ms, 50 ms, 150 ms, 500 ms, 1000 ms]
        """
        load_action = QtGui.QAction('&Load graph', self)
        load_action.setShortcut('Ctrl+L')
        load_action.triggered.connect(self.graph_gui.set_graph)

        kill_action = QtGui.QAction('&Kill search', self)
        kill_action.setShortcut('Ctrl+K')
        kill_action.triggered.connect(self.graph_gui.thread.end_search)

        exit_action = QtGui.QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(QtGui.qApp.quit)

        yes_action = QtGui.QAction('&Yes', self)
        yes_action.triggered.connect(
            lambda: self.graph_gui.set_vertex_numbering(True)
        )

        no_action = QtGui.QAction('&No', self)
        no_action.triggered.connect(
            lambda: self.graph_gui.set_vertex_numbering(False)
        )

        menu = self.menuBar()
        file_menu = menu.addMenu('&File')
        file_menu.addAction(load_action)
        file_menu.addAction(kill_action)
        file_menu.addAction(exit_action)

        numbering_menu = menu.addMenu('&Vertex Numbers')
        numbering_menu.addAction(yes_action)
        numbering_menu.addAction(no_action)

        delay_menu = menu.addMenu('&Delay')
        delays = [0, 50, 150, 500, 1000]
        for delay in delays:
            delay_action = QtGui.QAction('&' + str(delay) + ' ms', self)
            expr = 'self.graph_gui.set_delay({})'.format(delay)
            delay_action.triggered.connect(make_function([], expr, locals()))
            delay_menu.addAction(delay_action)

    def init_toolbar(self):
        """ Initializes a toolbar, with a run button and delay controls """
        play_icon = QtGui.QIcon(res.imgs.__path__[0]  + '/play.png')
        run_action = QtGui.QAction(play_icon, 'Run search', self)
        run_action.setShortcut('Ctrl+R')
        run_action.setStatusTip('Run search')
        run_action.triggered.connect(self.graph_gui.start_search)

        toolbar = self.addToolBar('Run')
        toolbar.addAction(run_action)
        for i in range(3, 11):
            color_action = QtGui.QAction('Colors ' + str(i), self)
            expr = 'self.graph_gui.set_color({})'.format(i)
            color_action.triggered.connect(make_function([], expr, locals()))
            toolbar.addAction(color_action)


def main():
    """ Creates Qt app and loads default level """
    import sys
    app = QtGui.QApplication(sys.argv)

    _ = MainWindow()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
