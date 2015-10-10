""" A GUI application for showing vertex coloring on graphs """
from PyQt4 import QtGui
from PyQt4.QtGui import QPixmap

import res.imgs
import res.play2048s
from src.utils.func import make_function
from src.modules.module4.play_2048_gui import Play2048GUI


class MainWindow(QtGui.QMainWindow):
    """ The GUI window which contains the Widgets and buttons """

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.gui = Play2048GUI(self)
        self.screenshot_count = 0
        self.init_ui()

    def init_ui(self):
        """ Initializes the UI, delegates to init_menubar and init_toolbar """
        self.setCentralWidget(self.gui)

        self.init_menubar()
        self.init_toolbar()

        status_bar_label = QtGui.QLabel()
        self.statusBar().addWidget(status_bar_label)

        score_label = QtGui.QLabel()
        self.statusBar().addPermanentWidget(score_label)

        self.gui.status_message[str].connect(status_bar_label.setText)
        self.gui.score_message[str].connect(score_label.setText)
        self.gui.screenshot.connect(self.shoot)

        self.show()
        self.raise_()

    def init_menubar(self):
        """ Initializes a menubar with the following items:
        File -> [ Kill, Reset, Exit ]
        Delay -> [ 10 ms, 50 ms, 150 ms, 500 ms, 1000 ms, 2000 ms ]
        Screenshots -> [ On, Off ]
        Depth -> [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
        Heuristic -> [ Random, Snake, Corner, Log, Ov3y ]
        """
        menu = self.menuBar()
        file_menu = menu.addMenu('&File')
        delay_menu = menu.addMenu('&Delay')
        screenshots_menu = menu.addMenu('&Screenshots')
        depth_menu = menu.addMenu('&Depth')
        heuristic_menu = menu.addMenu('&Heuristic')

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

        delays = [0, 50, 150, 500, 1000, 2000]
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

        depths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for depth in depths:
            depth_action = QtGui.QAction('&' + str(depth), self)
            expr = 'self.gui.set_depth({})'.format(depth)
            depth_action.triggered.connect(make_function([], expr, locals()))
            depth_menu.addAction(depth_action)

        heuristics = ['Random', 'Snake', 'Corner', 'LogGradient', 'Ov3y']
        for heuristic in heuristics:
            heuristic_action = QtGui.QAction('&' + heuristic, self)
            exp = 'self.gui.set_heuristic("{}")'.format(heuristic)
            heuristic_action.triggered.connect(make_function([], exp, locals()))
            heuristic_menu.addAction(heuristic_action)

    def init_toolbar(self):
        """ Initializes a toolbar, with a run button and delay controls """
        play_icon = QtGui.QIcon(res.imgs.__path__[0] + '/play.png')
        run_action = QtGui.QAction(play_icon, 'Run search', self)
        run_action.setShortcut('Ctrl+R')
        run_action.triggered.connect(self.gui.start_search)

        start_action = QtGui.QAction('&Play yourself', self)
        start_action.triggered.connect(self.gui.start_manual_game)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(run_action)
        toolbar.addAction(start_action)

    def shoot(self):
        path = res.play2048s.__path__[0]
        filename = '/screenshot-' + str(self.screenshot_count) + '.jpg'

        window = QPixmap.grabWidget(self.window())
        window.save(path + filename, 'jpg')
        self.screenshot_count += 1


def main():
    """ Creates Qt app and loads default level """
    import sys
    app = QtGui.QApplication(sys.argv)
    _ = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
