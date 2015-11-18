""" A GUI application for showing mnist classification results """
from PyQt4 import QtGui
from PyQt4.QtGui import QPixmap

import res.imgs
import res.mnist

from src.utils.func import make_function
from src.modules.module5.mnist_gui import MNISTGUI


class MainWindow(QtGui.QMainWindow):
    """ The GUI window which contains the Widgets and buttons """

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.gui = MNISTGUI(self)
        self.init_ui()
        welcome_message = 'Welcome! Lets classify those bitches...'
        self.gui.status_message.emit(welcome_message)

    def init_ui(self):
        """ Initializes the UI, delegates to init_menubar and init_toolbar """
        self.setCentralWidget(self.gui)

        #self.init_menubar()
        self.init_toolbar()

        status_bar_label = QtGui.QLabel()
        self.statusBar().addWidget(status_bar_label)

        score_label = QtGui.QLabel()
        self.statusBar().addPermanentWidget(score_label)

        self.gui.status_message[str].connect(status_bar_label.setText)
        self.gui.score_message[str].connect(score_label.setText)

        self.show()
        self.raise_()

    def init_menubar(self):
        """ Initializes a menubar with the following items:
        File -> [ Kill, Reset, Exit ]
        Delay -> [ 10 ms, 50 ms, 150 ms, 500 ms ]
        Screenshots -> [ On, Off ]
        Depth -> [ 2, 3, 4 ]
        """
        menu = self.menuBar()
        file_menu = menu.addMenu('&File')
        delay_menu = menu.addMenu('&Delay')
        screenshots_menu = menu.addMenu('&Screenshots')
        depth_menu = menu.addMenu('&Depth')

        kill_action = QtGui.QAction('&Kill game', self)
        kill_action.setShortcut('Ctrl+K')
        kill_action.triggered.connect(self.gui.end_search)
        file_menu.addAction(kill_action)

        reset_size_action = QtGui.QAction('&Reset size', self)
        reset_size_action.triggered.connect(self.gui.reset_size)
        file_menu.addAction(reset_size_action)

        exit_action = QtGui.QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(QtGui.qApp.quit)
        file_menu.addAction(exit_action)

        delays = [0, 50, 150, 500]
        for delay in delays:
            delay_action = QtGui.QAction('&' + str(delay) + ' ms', self)
            expr = 'self.gui.set_delay({})'.format(delay)
            delay_action.triggered.connect(make_function([], expr, locals()))
            delay_menu.addAction(delay_action)

        screens_on = QtGui.QAction('&On', self)
        screens_on.triggered.connect(lambda: self.gui.set_screenshots(True))
        screenshots_menu.addAction(screens_on)

        screens_off = QtGui.QAction('&Off', self)
        screens_off.triggered.connect(lambda: self.gui.set_screenshots(False))
        screenshots_menu.addAction(screens_off)

        depths = [2, 3, 4]
        for depth in depths:
            depth_action = QtGui.QAction('&' + str(depth), self)
            expr = 'self.gui.set_depth({})'.format(depth)
            depth_action.triggered.connect(make_function([], expr, locals()))
            depth_menu.addAction(depth_action)

    def init_toolbar(self):
        """ Initializes a toolbar, with a run button and delay controls """
        run_icon = QtGui.QIcon(res.imgs.__path__[0] + '/play.png')
        run_action = QtGui.QAction(run_icon, 'Run training', self)
        run_action.setShortcut('Ctrl+R')
        run_action.triggered.connect(self.gui.start_training)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(run_action)


def main():
    """ Creates Qt app """
    import sys
    app = QtGui.QApplication(sys.argv)
    _ = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
