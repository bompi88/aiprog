""" A Widget for drawing Graph states """
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal

from src.puzzles.play_2048.play_2048 import Play2048
from src.puzzles.play_2048.play_2048_player import Play2048Player


class Play2048GUI(QtGui.QFrame):
    """ Implement QFrame, which is a subclass of QWidget """
    status_message = pyqtSignal(str)
    score_message = pyqtSignal(str)

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)

        self.tile_size = 1
        self.tiles = 4
        self.widget_size_px = 600

        self.player = Play2048Player(self)

        self.splash_screen = [[4096, 2048, 512, 64], [1024, 256, 32, 0],
                              [128, 16, 2, 0], [8, 4, 0, 8192]]

        self.started = False
        self.game_state = None
        self.set_game()
        self.delay = 50
        self.init_ui()
        self.colors = None
        self.init_colors()

    def init_ui(self):
        """ Initialize the UI """
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        size = QtCore.QSize(self.widget_size_px, self.widget_size_px)
        self.setMinimumSize(size)
        self.parent().adjustSize()
        self.parent().setWindowTitle('Module 4 - 2048')
        self.status_message.emit(str('Welcome'))

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

    def level_loaded(self, game):
        """ Called whenever a level is loaded, adjust Widget size """
        self.game_state = game

        self.compute_tile_size()

    def compute_tile_size(self):
        """ Computes tile size based on widget size and nonogram """
        self.tile_size = 1

        self.tile_size *= (self.widget_size_px / float(self.tiles))

    def start_search(self):
        """ Start the search in the worker thread """
        if self.started:
            self.player = Play2048Player(self)
            self.level_loaded(Play2048())
            self.player.score = 0
        self.status_message.emit(str('Search started'))
        self.started = True
        self.player.play(self.game_state)
        self.update()

    def paintEvent(self, _):  # pylint: disable=invalid-name
        """ Called by the Qt event loop when the widget should be updated """
        painter = QtGui.QPainter(self)

        board = self.game_state.board if self.started else self.splash_screen

        self.paint_board(painter, board)
        self.paint_outer_border(painter)

    def resizeEvent(self, e):  # pylint: disable=invalid-name
        """ Handles widget resize and scales Nonogram """
        size = max(e.size().width(), e.size().height())
        self.widget_size_px = size
        self.compute_tile_size()

    def keyReleaseEvent(self, e):  # pylint: disable=invalid-name
        key = e.key()

        direction_keys = {16777234: 'Left',
                          16777235: 'Up',
                          16777236: 'Right',
                          16777237: 'Down'}

        if key in direction_keys:
            moves = {
                'Left': [-1, 0], 'Up': [0, -1], 'Right': [1, 0], 'Down': [0, 1]
            }
            self.do_move(moves[direction_keys[key]])

    def paint_board(self, painter, board):
        """ Draws a Nonogram, WHITE should be treated as an error. """

        off_whites = [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]

        for y, row in enumerate(board):
            for x, element in enumerate(row):
                border_width = self.widget_size_px / 60.0
                pen_brush = QtGui.QBrush(self.colors['grid_color'])
                painter.setPen(QtGui.QPen(pen_brush, border_width))

                if element <= 2048:
                    painter.setBrush(self.colors[int(element)])
                else:
                    painter.setBrush(self.colors['super'])

                painter.drawRect(self.tile_size * x, self.tile_size * y,
                                 self.tile_size - 1, self.tile_size - 1)

                if element in off_whites:
                    painter.setPen(self.colors['off_white'])
                else:
                    painter.setPen(self.colors['text_color'])

                font_size = self.widget_size_px / 12.0
                font = painter.font()
                font.setPointSize(font_size)
                painter.setFont(font)

                x_base_offset = self.widget_size_px / 33.0
                x_char_offset = self.widget_size_px / 40.0
                x_offset = x_base_offset + (
                    (4 - len(str(element))) * x_char_offset)
                y_base_offset = self.widget_size_px / 40.0
                y_offset = (self.widget_size_px / (4 * 2.0)) + y_base_offset
                text_point = QtCore.QPoint(x * self.tile_size + x_offset,
                                           y * self.tile_size + y_offset)
                painter.drawText(text_point, str(element))

    def paint_outer_border(self, painter):
        border_width = self.widget_size_px / 60.0

        painter.setBrush(QtCore.Qt.transparent)
        pen_brush = QtGui.QBrush(self.colors['grid_color'])
        painter.setPen(QtGui.QPen(pen_brush, 2 * border_width))
        x = y = self.widget_size_px - 1
        painter.drawRect(0, 0, x, y)

    def set_game(self):
        game = Play2048()

        self.level_loaded(game)

        self.update()

    def set_delay(self, delay):
        """ Change delay """
        self.delay = delay
        self.status_message.emit('Delay: ' + str(delay))

    def start_manual_game(self):
        if not self.started:
            self.started = True
            self.player.game = self.game_state
        else:
            self.level_loaded(Play2048())
            self.player.score = 0

        self.update()

    def do_move(self, move):
        if not self.player.game:
            self.started = True
            self.player.game = self.game_state
        did_move = self.player.move(move)
        if did_move:
            self.player.game.next_state()

        self.score_message.emit('Score: {}'.format(self.player.score))

        if not self.player.is_possible():
            self.status_message.emit('Finished')
        self.update()
