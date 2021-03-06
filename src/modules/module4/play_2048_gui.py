""" A Widget for drawing Graph states """
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal

from src.modules.module4.utils.play_2048_worker import Play2048Worker
from src.modules.module4.utils.play_2048_manual import Play2048Manual
from src.modules.module4.utils.play_2048_test_worker import Play2048TestWorker
from src.modules.module4.utils.play_2048_train_worker import Play2048TrainWorker
from src.modules.module4.utils.play_2048_save_worker import Play2048SaveWorker
from src.algorithms.adversial_search.expectimax_c import ExpectimaxC

from src.puzzles.play_2048.play_2048_player import Play2048Player

from math import log
import pickle
import time
import os
import res.play2048s
import res.play2048s.ai_runs


class Play2048GUI(QtGui.QFrame):
    """ Implement QFrame, which is a subclass of QWidget """
    status_message = pyqtSignal(str)
    score_message = pyqtSignal(str)
    screenshot = pyqtSignal()

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)

        self.depth = 2
        self.search = ExpectimaxC
        self.net = None

        self.delay = 50
        self.heuristic = 0
        self.epochs = 100
        self.num_cases = 10000
        self.worker = None
        self.started = False
        self.manual_mode = None

        self.tile_size = 1
        self.border_width = 0
        self.tiles = 4
        self.widget_size_px = 600
        self.font_size = 0
        self.set_ui_utilities()
        self.init_ui()
        self.colors = None
        self.init_colors()

        self.take_screenshots = False
        self.pickle_states = False
        self.min_save_tiles = 10
        self.reload_saves = True
        self.states = {}

        self.move_keys = {0: 'left', 1: 'up', 2: 'right', 3: 'down'}

        self.splash_screen = [
            4096, 2048, 512, 64,
            1024, 256, 32, 0,
            128, 16, 2, 0,
            8, 4, 0, 8192
        ]

        for i, el in enumerate(self.splash_screen):
            if el is 0:
                continue

            self.splash_screen[i] = int(log(el, 2))

    def init_ui(self):
        """ Initialize the UI """
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        size = QtCore.QSize(self.widget_size_px, self.widget_size_px)
        self.setMinimumSize(size)
        self.parent().adjustSize()
        self.parent().setWindowTitle('Module 4 - 2048')

    def init_colors(self):
        self.colors = {
            0: QtGui.QColor('#cdc1b5'),
            2: QtGui.QColor('#eee4da'),
            4: QtGui.QColor('#ede0c8'),
            8: QtGui.QColor('#f2b179'),
            16: QtGui.QColor('#f59563'),
            32: QtGui.QColor('#f67c5f'),
            64: QtGui.QColor('#f65e3b'),
            128: QtGui.QColor('#edcf72'),
            256: QtGui.QColor('#edcc61'),
            512: QtGui.QColor('#edc850'),
            1024: QtGui.QColor('#edc53f'),
            2048: QtGui.QColor('#edc22e'),
            'super': QtGui.QColor('#3c3a32'),
            'off_white': QtGui.QColor('#f9f6f2'),
            'grid_color': QtGui.QColor('#bbada0'),
            'text_color': QtGui.QColor('#776e65')
        }

    def set_ui_utilities(self):
        """ Computes tile size based on widget size and nonogram """
        self.tile_size = 1

        self.tile_size *= (self.widget_size_px / float(self.tiles))

        self.font_size = self.widget_size_px / 12.0
        self.border_width = self.widget_size_px / 60.0

    def start_search(self):
        """ Start the search in the worker thread """
        self.end_process()
        self.start()

    def game_ended(self):
        self.status_message.emit('Game ended')
        if self.take_screenshots:
            self.parent().animate()

        if self.pickle_states:
            path = res.play2048s.__path__[0] + '/'
            filename = str(round(time.time())) + '.p'
            f = open(path + filename, 'wb')
            pickle.dump(self.worker.states, f)
            self.pickle_states = False

    def single_save_ended(self, tile=None):
        path = res.play2048s.ai_runs.__path__[0] + '/'
        filename = str(2 ** tile) + '_' + str(self.heuristic) if tile else str(round(time.time()))
        filename += '.p'

        if self.reload_saves:
            self.states = {}

        if tile:
            if self.reload_saves:
                has_file = False
                if os.path.exists(path + filename):
                    has_file = True

                if has_file:
                    fr = open(path + filename, 'rb')
                    while 1:
                        try:
                            z = self.states.get(tile, {})
                            z.update(pickle.load(fr))
                            self.states[tile] = z
                        except EOFError:
                            break
                    fr.close()
        else:
            tile = 1

        p = self.states.get(tile, {})
        p.update(self.worker.states)
        self.states[tile] = p

        fw = open(path + filename, 'wb')

        pickle.dump(self.states[tile], fw)
        fw.close()

    def save_ended(self):
        self.status_message.emit('Saving states finished')

    def training_ended(self):
        self.status_message.emit('Training finished')

    def testing_ended(self):
        self.status_message.emit('Testing finished')
        if self.take_screenshots:
            self.parent().animate()

    def start_manual_game(self):
        self.end_process()
        self.start(True)

    def start_test(self):
        self.end_process()

        self.worker = Play2048TestWorker(self, ann=self.net)
        self.worker.start()

        self.started = True
        self.update()

        self.status_message.emit(str('Test started'))

    def start_welch(self):
        self.end_process()

        self.worker = Play2048TestWorker(self, welch=True, ann=self.net)
        self.worker.start()

        self.started = True
        self.update()

        self.status_message.emit(str('Welch test started'))

    def start_training(self):
        self.end_process()

        self.worker = Play2048TrainWorker(self)
        self.worker.start()

        self.started = True
        self.update()

        self.status_message.emit(str('Training started'))

    def save_plays(self, num_plays):
        self.reload_saves = True
        self.end_process()

        self.worker = Play2048SaveWorker(self, num_plays, self.min_save_tiles)
        self.worker.start()

        self.started = True
        self.update()

        self.status_message.emit(str('Saving ' + str(num_plays) + ' plays'))

    def end_process(self):
        if not self.started:
            return

        if not self.manual_mode:
            self.worker.end_worker()
        self.worker = None
        self.started = False
        self.score_message.emit(str(''))
        self.status_message.emit(str(''))

    def start(self, manual=False):
        if self.started:
            return

        self.manual_mode = manual

        if manual:
            self.worker = Play2048Manual(self)
        else:
            self.worker = Play2048Worker(self)
            self.worker.start()

        self.started = True
        self.update()

        if manual:
            self.score_message.emit(str('Score: 0'))
            self.status_message.emit(str('Manual game play started'))
        else:
            self.status_message.emit(str('Search started'))

    def paintEvent(self, _):  # pylint: disable=invalid-name
        """ Called by the Qt event loop when the widget should be updated """
        painter = QtGui.QPainter(self)

        font = painter.font()
        font.setPointSize(self.font_size)
        painter.setFont(font)

        if getattr(self.worker, 'board', None):
            board = self.worker.board() if self.started else self.splash_screen
        else:
            board = self.splash_screen

        self.paint_board(painter, board)
        self.paint_outer_border(painter)

    def resizeEvent(self, e):  # pylint: disable=invalid-name
        """ Handles widget resize and scales Nonogram """
        size = max(e.size().width(), e.size().height())
        self.setMinimumSize(QtCore.QSize(size, size))
        self.widget_size_px = size
        self.set_ui_utilities()

    def reset_size(self):
        self.widget_size_px = 600
        self.setMinimumSize(QtCore.QSize(self.widget_size_px,
                                         self.widget_size_px))
        self.parent().adjustSize()
        self.update()

    def keyReleaseEvent(self, e):  # pylint: disable=invalid-name
        key = e.key() - 16777234

        if key in self.move_keys and self.manual_mode:
            move = self.move_keys[key]
            moves = Play2048Player.actions()

            self.worker.do_move(moves[move])

    def paint_board(self, painter, board):
        """ Draws a Nonogram, WHITE should be treated as an error. """

        x_offset = self.widget_size_px / 33.0
        x_char_offset = self.widget_size_px / 40.0
        y_offset = (3 * self.widget_size_px) / 20.0

        for y in range(4):
            for x in range(4):
                t = board[4 * y + x]
                element = 2 ** t if t is not 0 else 0

                pen_brush = QtGui.QBrush(self.colors['grid_color'])
                painter.setPen(QtGui.QPen(pen_brush, self.border_width))

                if element <= 2048:
                    painter.setBrush(self.colors[element])
                else:
                    painter.setBrush(self.colors['super'])

                painter.drawRect(self.tile_size * x, self.tile_size * y,
                                 self.tile_size - 1, self.tile_size - 1)

                if element >= 8:
                    painter.setPen(self.colors['off_white'])
                else:
                    painter.setPen(self.colors['text_color'])

                x_str_offset = (4 - len(str(element))) * x_char_offset

                text_x = x * self.tile_size + x_offset + x_str_offset
                text_y = y * self.tile_size + y_offset

                painter.drawText(text_x, text_y, str(element))

    def paint_outer_border(self, painter):
        border_width = self.widget_size_px / 60.0

        painter.setBrush(QtCore.Qt.transparent)
        pen_brush = QtGui.QBrush(self.colors['grid_color'])
        painter.setPen(QtGui.QPen(pen_brush, 2 * border_width))
        x = y = self.widget_size_px - 1
        painter.drawRect(0, 0, x, y)

    def set_delay(self, delay):
        """ Change delay """
        self.delay = delay
        self.status_message.emit('Delay: ' + str(delay))

    def set_depth(self, depth):
        self.depth = depth
        self.status_message.emit('Depth: ' + str(depth))

    def set_screenshots(self, take_screenshots):
        self.take_screenshots = take_screenshots
        if take_screenshots:
            self.status_message.emit('Taking screenshots')

    def set_pickling(self, do_pickle):
        self.pickle_states = do_pickle
        if do_pickle:
            self.status_message.emit('Saving game states')

    def set_min_save_tiles(self, min_tile):
        self.min_save_tiles = min_tile
        self.status_message.emit(
            'Saving / Using plays that has tiles greater than or equal ' + str(2 ** self.min_save_tiles)
        )

    def set_heuristic(self, heuristic):
        self.heuristic = heuristic
        self.status_message.emit('Using Heuristic ' + str(heuristic + 1))

    def set_epochs(self, epochs):
        self.epochs = epochs
        self.status_message.emit('Will use epochs of ' + str(epochs))

    def set_num_cases(self, num_cases):
        self.num_cases = num_cases
        self.status_message.emit('Number of cases to be used is ' + str(num_cases))

    @staticmethod
    def delete_states(tile):
        if not tile:
            return
        path = res.play2048s.ai_runs.__path__[0] + '/'
        filename = str(2 ** tile) + '.p'
        os.remove(path + filename)
