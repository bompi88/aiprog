""" A GUI application for showing vertex coloring on graphs """
import os
import sys

from PyQt4 import QtGui

import src.modules
from src.modules.module3.utils.nonogram_reader import NonogramReader
from src.modules.module3.nonogram_gui import NonogramGUI


class MainWindow(QtGui.QMainWindow):
    """ The GUI window which contains the Widgets and buttons """

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.nonogram_gui = NonogramGUI(self)

        self.init_ui()

    def init_ui(self):
        """ Initializes the UI, delegates to init_menubar and init_toolbar """
        self.setCentralWidget(self.nonogram_gui)

        self.init_menubar()
        self.init_toolbar()

        status_bar = self.statusBar()
        self.nonogram_gui.status_message[str].connect(
            status_bar.showMessage
        )

        self.center()
        self.show()
        self.raise_()

    def init_menubar(self):
        """ Initializes a menubar with the following items:
         File -> [ Load, Kill, Exit ]
        """
        load_action = QtGui.QAction('&Load graph', self)
        load_action.setShortcut('Ctrl+L')
        load_action.triggered.connect(
            lambda: self.nonogram_gui.set_graph(
                NonogramReader.load_level(self.nonogram_gui)
            )
        )

        kill_action = QtGui.QAction('&Kill search', self)
        kill_action.setShortcut('Ctrl+K')
        # kill_action.triggered.connect(self.nonogram_gui.thread.terminate)

        exit_action = QtGui.QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(QtGui.qApp.quit)

        menu = self.menuBar()
        menu.setNativeMenuBar(False)
        file_menu = menu.addMenu('&File')
        file_menu.addAction(load_action)
        file_menu.addAction(kill_action)
        file_menu.addAction(exit_action)

    def init_toolbar(self):
        """ Initializes a toolbar, with a run button and delay controls """
        path = os.path.dirname(src.modules.__file__)
        path += '/module1/res/'
        run_action = QtGui.QAction(QtGui.QIcon(path + 'play.png'), 'Run A*', self)
        run_action.setShortcut('Ctrl+R')
        run_action.setStatusTip('Run A*')
        run_action.triggered.connect(self.nonogram_gui.start_search)

        delay_action_0 = QtGui.QAction('Delay 0', self)
        delay_action_0.triggered.connect(
            lambda: self.nonogram_gui.set_delay(0) and self.delay_changed(0)
        )

        delay_action_50 = QtGui.QAction('Delay 50', self)
        delay_action_50.triggered.connect(
            lambda: self.nonogram_gui.set_delay(50) and self.delay_changed(50)
        )

        delay_action_150 = QtGui.QAction('Delay 150', self)
        delay_action_150.triggered.connect(
            lambda: self.nonogram_gui.set_delay(150) and self.delay_changed(150)
        )

        delay_action_500 = QtGui.QAction('Delay 500', self)
        delay_action_500.triggered.connect(
            lambda: self.nonogram_gui.set_delay(500) and self.delay_changed(500)
        )

        delay_action_1000 = QtGui.QAction('Delay 1000', self)
        delay_action_1000.triggered.connect(
            lambda: self.nonogram_gui.set_delay(1000) and self.delay_changed(1000)
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

    def delay_changed(self, delay):
        """ Writes to status bar when delay is changed """
        self.statusBar().showMessage('Delay: ' + str(delay))


def main():
    """ Creates Qt app and loads default level """
    app = QtGui.QApplication(sys.argv)

    main_window = MainWindow()
    filename, nonogram = list(NonogramReader.load_level(main_window.nonogram_gui))
    main_window.nonogram_gui.level_loaded(filename, nonogram)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
