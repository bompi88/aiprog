""" A GUI application for showing vertex coloring on graphs """
from PyQt4 import QtGui
from PyQt4.QtGui import QPixmap

import res.imgs
import res.play2048s
import src.clibs

from subprocess import call
from src.utils.func import make_function
from src.modules.module4.play_2048_gui import Play2048GUI


class MainWindow(QtGui.QMainWindow):
    """ The GUI window which contains the Widgets and buttons """

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.gui = Play2048GUI(self)
        self.screenshot_count = 0
        self.init_ui()
        welcome_message = 'Welcome! Depth: {}, Search: {}'.format(
            self.gui.depth,
            self.gui.search.__name__
        )
        self.gui.status_message.emit(welcome_message)

        # Compile c implementation of Expectimax
        call(['{}/compile.sh'.format(src.clibs.__path__[0])])

    def init_ui(self):
        """ Initializes the UI, delegates to init_menubar and init_toolbar """
        self.setCentralWidget(self.gui)

        self.init_menubar()
        self.init_toolbar()

        status_bar_label = QtGui.QLabel()
        status_bar_label.setWordWrap(True)
        status_bar_label.setFixedWidth(600)

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
        Delay -> [ 10 ms, 50 ms, 150 ms, 500 ms ]
        Screenshots -> [ On, Off ]
        Depth -> [ 2, 3, 4 ]
        """
        menu = self.menuBar()
        file_menu = menu.addMenu('&File')
        delay_menu = menu.addMenu('&Delay')
        screenshots_menu = menu.addMenu('&Screenshots')
        pickling_menu = menu.addMenu('&Save states')
        delete_state_menu = menu.addMenu('&Delete states')
        min_tile_menu = menu.addMenu('&Min tile')
        heuristics_menu = menu.addMenu('&Heuristics')
        depth_menu = menu.addMenu('&Depth')
        epochs_menu = menu.addMenu('&Epochs')
        num_cases_menu = menu.addMenu('&Number of cases')

        kill_action = QtGui.QAction('&Kill running process', self)
        kill_action.setShortcut('Ctrl+K')
        kill_action.triggered.connect(self.gui.end_process)
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

        pickling_on = QtGui.QAction('&On', self)
        pickling_on.triggered.connect(lambda: self.gui.set_pickling(True))
        pickling_menu.addAction(pickling_on)

        pickling_off = QtGui.QAction('&Off', self)
        pickling_off.triggered.connect(lambda: self.gui.set_pickling(False))
        pickling_menu.addAction(pickling_off)

        depths = [2, 3, 4]
        for depth in depths:
            depth_action = QtGui.QAction('&' + str(depth), self)
            expr = 'self.gui.set_depth({})'.format(depth)
            depth_action.triggered.connect(make_function([], expr, locals()))
            depth_menu.addAction(depth_action)

        min_tiles = [7, 8, 9, 10, 11, 12]
        for min_tile in min_tiles:
            min_tile_action = QtGui.QAction('&' + str(2 ** min_tile), self)
            expr = 'self.gui.set_min_save_tiles({})'.format(min_tile)
            min_tile_action.triggered.connect(make_function([], expr, locals()))
            min_tile_menu.addAction(min_tile_action)

        delete_states = [7, 8, 9, 10, 11, 12]
        for delete_state in delete_states:
            delete_state_action = QtGui.QAction('&' + str(2 ** delete_state), self)
            expr = 'self.gui.delete_states({})'.format(delete_state)
            delete_state_action.triggered.connect(make_function([], expr, locals()))
            delete_state_menu.addAction(delete_state_action)

        heuristics = [0, 1]
        for heuristic in heuristics:
            heuristics_action = QtGui.QAction('&Heuristic ' + str(heuristic + 1), self)
            expr = 'self.gui.set_heuristic({})'.format(heuristic)
            heuristics_action.triggered.connect(make_function([], expr, locals()))
            heuristics_menu.addAction(heuristics_action)

        epochs = [10, 30, 60, 100, 200, 300, 500, 1000, 2000, 3000, 4000, 5000, 10000]
        for epoch in epochs:
            epoch_action = QtGui.QAction('&' + str(epoch), self)
            expr = 'self.gui.set_epochs({})'.format(epoch)
            epoch_action.triggered.connect(make_function([], expr, locals()))
            epochs_menu.addAction(epoch_action)

        num_cases_items = [10, 100, 500, 1000, 5000, 10000, 20000, 30000, 40000, 50000, 60000]
        for num_cases in num_cases_items:
            num_cases_action = QtGui.QAction('&' + str(num_cases), self)
            expr = 'self.gui.set_num_cases({})'.format(num_cases)
            num_cases_action.triggered.connect(make_function([], expr, locals()))
            num_cases_menu.addAction(num_cases_action)

    def init_toolbar(self):
        """ Initializes a toolbar, with a run button and delay controls """
        play_icon = QtGui.QIcon(res.imgs.__path__[0] + '/play.png')
        run_action = QtGui.QAction(play_icon, 'Run search', self)
        run_action.setShortcut('Ctrl+R')
        run_action.triggered.connect(self.gui.start_search)

        start_action = QtGui.QAction('&Play yourself', self)
        start_action.triggered.connect(self.gui.start_manual_game)

        train_action = QtGui.QAction('&Train', self)
        train_action.triggered.connect(self.gui.start_training)

        test_action = QtGui.QAction('&Test', self)
        test_action.triggered.connect(self.gui.start_test)

        welch_action = QtGui.QAction('&Welch', self)
        welch_action.triggered.connect(self.gui.start_welch)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(run_action)
        toolbar.addAction(start_action)
        toolbar.addAction(train_action)
        toolbar.addAction(test_action)
        toolbar.addAction(welch_action)

        save_num_plays = [100, 1000, 10000, 30000]
        for save_plays in save_num_plays:
            save_plays_action = QtGui.QAction('&Save ' + str(save_plays), self)
            expr = 'self.gui.save_plays({})'.format(save_plays)
            save_plays_action.triggered.connect(make_function([], expr, locals()))
            toolbar.addAction(save_plays_action)

    def shoot(self):
        path = res.play2048s.__path__[0]
        filename = '/screenshot-' + str(self.screenshot_count).zfill(6) + '.jpg'

        window = QPixmap.grabWidget(self.window())
        window.save(path + filename, 'jpg')
        self.screenshot_count += 1

    def animate(self):
        path = res.play2048s.__path__[0] + '/'
        screenshots = path + '*.jpg'
        gif = path + 'animated.gif'
        cmd = 'convert -delay 15 -loop 1 -colors 256 -layers Optimize '
        cmd += '{} {}'.format(screenshots, gif)

        call([cmd], shell=True)
        self.gui.status_message.emit('Created gif')


def main():
    """ Creates Qt app and loads default level """
    import sys
    app = QtGui.QApplication(sys.argv)
    _ = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
