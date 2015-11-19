""" A GUI application for showing mnist classification results """
from PyQt4 import QtGui

import res.imgs
import res.mnist

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

        self.init_menubar()
        self.init_toolbar()

        status_bar_label = QtGui.QLabel()
        status_bar_label.setWordWrap(True)
        status_bar_label.setFixedWidth(600)

        self.statusBar().addWidget(status_bar_label)

        self.gui.status_message[str].connect(status_bar_label.setText)

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

        open_action = QtGui.QAction('&Open', self)
        open_action.setShortcut('Ctrl+K')
        open_action.triggered.connect(self.gui.open)
        file_menu.addAction(open_action)

        save_action = QtGui.QAction('&Save', self)
        save_action.setShortcut('Ctrl+K')
        save_action.triggered.connect(self.gui.save)
        file_menu.addAction(save_action)

        kill_action = QtGui.QAction('&Kill game', self)
        kill_action.setShortcut('Ctrl+K')
        kill_action.triggered.connect(self.gui.end)
        file_menu.addAction(kill_action)

        exit_action = QtGui.QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(QtGui.qApp.quit)
        file_menu.addAction(exit_action)

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
