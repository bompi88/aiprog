""" A Widget for drawing Graph states """
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal

from src.modules.module4.utils.play_2048_worker import Play2048Worker
from src.modules.module4.utils.play_2048_manual import Play2048Manual
from src.algorithms.adversial_search.minimax import Minimax
from src.algorithms.adversial_search.minimax_alpha_beta import MinimaxAlphaBeta
from src.algorithms.adversial_search.expectimax import Expectimax
from src.algorithms.adversial_search.expectimax_c import ExpectimaxC

from src.puzzles.play_2048.play_2048_player import Play2048Player
from src.puzzles.play_2048.heuristics.random_move import RandomMove
from src.puzzles.play_2048.heuristics.snake_gradient import SnakeGradient
from src.puzzles.play_2048.heuristics.corner_gradient import CornerGradient
from src.puzzles.play_2048.heuristics.ov3y import Ov3y

from math import log


class Play2048GUI(QtGui.QFrame):
    """ Implement QFrame, which is a subclass of QWidget """
    status_message = pyqtSignal(str)
    score_message = pyqtSignal(str)
    screenshot = pyqtSignal()

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)

        self.depth = 2
        self.heuristic = RandomMove
        self.search = ExpectimaxC

        self.delay = 50
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
        self.end_search()
        self.start()

    def start_manual_game(self):
        self.start(True)

    def end_search(self):
        if not self.started:
            return

        if not self.manual_mode:
            self.worker.end_worker()
        self.worker = None
        self.started = False

    def start(self, manual=False):
        if self.started:
            return

        self.manual_mode = manual

        if manual:
            self.worker = Play2048Manual(self)
        else:
            self.worker = Play2048Worker(self, self.heuristic)
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

        board = self.worker.board() if self.started else self.splash_screen

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

    def set_heuristic(self, heuristic):
        if heuristic == 'Random':
            self.heuristic = RandomMove
        elif heuristic == 'Snake':
            self.heuristic = SnakeGradient
        elif heuristic == 'Corner':
            self.heuristic = CornerGradient
        elif heuristic == 'Ov3y':
            self.heuristic = Ov3y

        self.status_message.emit('Heuristic: ' + self.heuristic.__name__)

    def set_search_type(self, search_type):
        if search_type == 'Minimax':
            self.search = Minimax
        elif search_type == 'MinimaxAlphaBeta':
            self.search = MinimaxAlphaBeta
        elif search_type == 'Expectimax':
            self.search = Expectimax
        elif search_type == 'Expectimax C':
            self.search = ExpectimaxC

        self.status_message.emit('Search: ' + self.search.__name__)

    def set_screenshots(self, take_screenshots):
        self.take_screenshots = take_screenshots
        if take_screenshots:
            self.status_message.emit('Taking screenshots')
