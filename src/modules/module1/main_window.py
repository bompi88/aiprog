""" A GUI application for showing A* runs """
from PyQt4 import QtGui

import res.imgs
from src.utils.const import C
from src.modules.module1.navigation_gui import NavigationGUI


class MainWindow(QtGui.QMainWindow):
    """ The GUI window which contains the Widgets and buttons """

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.nav_gui = NavigationGUI(self)

        self.init_ui()

    def init_ui(self):
        """ Initializes the UI, delegates to init_menubar and init_toolbar """
        self.setCentralWidget(self.nav_gui)

        self.init_menubar()
        self.init_toolbar()

        status_bar = self.statusBar()
        self.nav_gui.status_message[str].connect(
            status_bar.showMessage
        )

        self.center()
        self.show()
        self.raise_()

    def init_menubar(self):
        """ Initializes a menubar with the following items:
         File -> [ Load, Kill, Exit ]
         Mode -> [ A*, DFS, BFS ]
        """
        load_action = QtGui.QAction('&Load map', self)
        load_action.setShortcut('Ctrl+L')
        load_action.triggered.connect(self.nav_gui.set_map)

        kill_action = QtGui.QAction('&Kill search', self)
        kill_action.setShortcut('Ctrl+K')
        kill_action.triggered.connect(self.nav_gui.thread.terminate)

        exit_action = QtGui.QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(QtGui.qApp.quit)

        a_star_action = QtGui.QAction('&A* Mode', self)
        a_star_action.setShortcut('Ctrl+1')
        a_star_action.triggered.connect(
            lambda: (self.nav_gui.set_mode(C.search_mode.A_STAR) and
                     self.mode_changed(C.search_mode.A_STAR))
        )

        dfs_action = QtGui.QAction('&DFS Mode', self)
        dfs_action.setShortcut('Ctrl+2')
        dfs_action.triggered.connect(
            lambda: (self.nav_gui.set_mode(C.search_mode.DFS) and
                     self.mode_changed(C.search_mode.DFS))
        )

        bfs_action = QtGui.QAction('&BFS Mode', self)
        bfs_action.setShortcut('Ctrl+3')
        bfs_action.triggered.connect(
            lambda: (self.nav_gui.set_mode(C.search_mode.BFS) and
                     self.mode_changed(C.search_mode.BFS))
        )

        diagonal_on = QtGui.QAction('&On', self)
        diagonal_on.triggered.connect(
            lambda: (self.nav_gui.set_diagonal(True) and
                     self.diagonal_changed(True))
        )

        diagonal_off = QtGui.QAction('&Off', self)
        diagonal_off.triggered.connect(
            lambda: (self.nav_gui.set_diagonal(False) and
                     self.diagonal_changed(False))
        )

        euclidean_option = QtGui.QAction('&Euclidean distance', self)
        euclidean_option.triggered.connect(
            lambda: (self.nav_gui.set_heuristics_type('euclidean') and
                     self.heuristics_changed('Euclidean distance'))
        )

        manhattan_option = QtGui.QAction('&Manhattan distance', self)
        manhattan_option.triggered.connect(
            lambda: (self.nav_gui.set_heuristics_type('manhattan') and
                     self.heuristics_changed('Manhattan distance'))
        )

        menu = self.menuBar()
        menu.setNativeMenuBar(False)
        file_menu = menu.addMenu('&File')
        file_menu.addAction(load_action)
        file_menu.addAction(kill_action)
        file_menu.addAction(exit_action)

        mode_menu = menu.addMenu('&Mode')
        mode_menu.addAction(a_star_action)
        mode_menu.addAction(dfs_action)
        mode_menu.addAction(bfs_action)

        diagonal_menu = menu.addMenu('&Diagonal')
        diagonal_menu.addAction(diagonal_on)
        diagonal_menu.addAction(diagonal_off)

        heuristics_menu = menu.addMenu('&Heuristics')
        heuristics_menu.addAction(euclidean_option)
        heuristics_menu.addAction(manhattan_option)

    def init_toolbar(self):
        """ Initializes a toolbar, with a run button and delay controls """
        play_icon = QtGui.QIcon(res.imgs.__path__[0] + '/play.png')
        run_action = QtGui.QAction(play_icon, 'Run search', self)
        run_action.setShortcut('Ctrl+R')
        run_action.setStatusTip('Run search')
        run_action.triggered.connect(self.nav_gui.start_search)

        delay_action_0 = QtGui.QAction('Delay 0', self)
        delay_action_0.triggered.connect(
            lambda: self.nav_gui.set_delay(0) and self.delay_changed(0)
        )

        delay_action_50 = QtGui.QAction('Delay 50', self)
        delay_action_50.triggered.connect(
            lambda: self.nav_gui.set_delay(50) and self.delay_changed(50)
        )

        delay_action_150 = QtGui.QAction('Delay 150', self)
        delay_action_150.triggered.connect(
            lambda: self.nav_gui.set_delay(150) and self.delay_changed(150)
        )

        delay_action_500 = QtGui.QAction('Delay 500', self)
        delay_action_500.triggered.connect(
            lambda: self.nav_gui.set_delay(500) and self.delay_changed(500)
        )

        delay_action_1000 = QtGui.QAction('Delay 1000', self)
        delay_action_1000.triggered.connect(
            lambda: self.nav_gui.set_delay(1000) and self.delay_changed(1000)
        )

        toolbar = self.addToolBar('Run')
        toolbar.addAction(run_action)
        toolbar.addAction(delay_action_0)
        toolbar.addAction(delay_action_50)
        toolbar.addAction(delay_action_150)
        toolbar.addAction(delay_action_500)
        toolbar.addAction(delay_action_1000)

    def center(self):
        """ Center window  [http://zetcode.com/gui/pyqt4/firstprograms/] """
        geometry = self.frameGeometry()
        desktop_center = QtGui.QDesktopWidget().availableGeometry().center()
        geometry.moveCenter(desktop_center)
        self.move(geometry.topLeft())

    def mode_changed(self, mode):
        """ Writes to status bar when mode is changed """
        mode_s = {
            C.search_mode.A_STAR: 'A*',
            C.search_mode.BFS: 'BFS',
            C.search_mode.DFS: 'DFS'
        }[mode]

        self.statusBar().showMessage('Mode: ' + mode_s)

    def delay_changed(self, delay):
        """ Writes to status bar when delay is changed """
        self.statusBar().showMessage('Delay: ' + str(delay))

    def diagonal_changed(self, is_diagonal):
        """ Writes to status bar when diagonal option has changed """
        self.statusBar().showMessage('Diagonal mode: ' + str(is_diagonal))

    def heuristics_changed(self, heuristics_type):
        """ Writes to status bar when heuristics option has changed """
        self.statusBar().showMessage('Heuristics: ' + str(heuristics_type))


def main():
    """ Creates Qt app and loads default level """
    import sys
    app = QtGui.QApplication(sys.argv)

    _ = MainWindow()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
