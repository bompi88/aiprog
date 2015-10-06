""" A GUI application for showing vertex coloring on graphs """
from PyQt4 import QtGui

import res.imgs
from src.utils.func import make_function
from src.modules.module4.play_2048_gui import Play2048GUI


class MainWindow(QtGui.QMainWindow):
    """ The GUI window which contains the Widgets and buttons """

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.gui = Play2048GUI(self)

        self.init_ui()

    def init_ui(self):
        """ Initializes the UI, delegates to init_menubar and init_toolbar """
        self.setCentralWidget(self.gui)

        self.init_menubar()
        self.init_toolbar()

        status_bar_label = QtGui.QLabel()
        status_bar_label.setWordWrap(True)
        status_bar_label.setFixedWidth(self.gui.widget_size_px)

        self.statusBar().addWidget(status_bar_label)
        self.gui.status_message[str].connect(status_bar_label.setText)

        self.show()
        self.raise_()

    def init_menubar(self):
        """ Initializes a menubar with the following items:
         File -> [ Kill, Exit ]
        """
        kill_action = QtGui.QAction('&Kill game', self)
        kill_action.setShortcut('Ctrl+K')
        kill_action.triggered.connect(self.gui.player.end_player)

        exit_action = QtGui.QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(QtGui.qApp.quit)

        menu = self.menuBar()
        file_menu = menu.addMenu('&File')
        file_menu.addAction(kill_action)
        file_menu.addAction(exit_action)

        delay_menu = menu.addMenu('&Delay')
        delays = [0, 50, 150, 500, 1000]
        for delay in delays:
            delay_action = QtGui.QAction('&' + str(delay) + ' ms', self)
            expr = 'self.gui.set_delay({})'.format(delay)
            delay_action.triggered.connect(make_function([], expr, locals()))
            delay_menu.addAction(delay_action)

    def init_toolbar(self):
        """ Initializes a toolbar, with a run button and delay controls """
        play_icon = QtGui.QIcon(res.imgs.__path__[0] + '/play.png')
        run_action = QtGui.QAction(play_icon, 'Run search', self)
        run_action.setShortcut('Ctrl+R')
        run_action.triggered.connect(self.gui.start_search)

        toolbar = self.addToolBar('Run')
        toolbar.addAction(run_action)

        start_action = QtGui.QAction('&Start Manual', self)
        start_action.setShortcut('Ctrl+s')
        start_action.triggered.connect(self.gui.start_manual_game)
        toolbar.addAction(start_action)

        moves = {
            'Left': [-1, 0], 'Up': [0, -1], 'Right': [1, 0], 'Down': [0, 1]
        }

        for name, move in moves.items():
            move_action = QtGui.QAction('&' + name, self)
            expr = 'self.gui.do_move({})'.format(move)
            move_action.setShortcut('Ctrl+' + name)
            move_action.triggered.connect(make_function([], expr, locals()))
            toolbar.addAction(move_action)

def main():
    """ Creates Qt app and loads default level """
    import sys
    app = QtGui.QApplication(sys.argv)
    _ = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
