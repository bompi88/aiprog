""" A Widget for drawing Graph states """
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal

from src.puzzles.nonogram.nonogram_bfs import NonogramBfs
from src.puzzles.nonogram.nonogram_state import NonogramState
from src.puzzles.nonogram.nonogram import Nonogram
from src.utils.const import C
from src.utils.search_worker import SearchWorker
import res.nonograms


class NonogramGUI(QtGui.QFrame):
    """ Implement QFrame, which is a subclass of QWidget """
    status_message = pyqtSignal(str)

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)

        self.dx = self.dy = 1
        self.widget_width_px = self.widget_height_px = 600

        self.nonogram_state = None
        self.set_nonogram(True)
        self.delay = 50
        self.mode = C.search_mode.A_STAR
        self.thread = SearchWorker(self)
        self.init_ui()

    def init_ui(self):
        """ Initialize the UI """
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        size = QtCore.QSize(self.widget_width_px, self.widget_height_px)
        self.setMinimumSize(size)
        self.parent().adjustSize()

    def level_loaded(self, nonogram):
        """ Called whenever a level is loaded, adjust Widget size """
        self.nonogram_state = NonogramState(nonogram, None)

        self.compute_tile_size()

    def compute_tile_size(self):
        """ Computes tile size based on widget size and nonogram """
        self.dx = self.dy = 1
        x, y = self.nonogram_state.state.x, self.nonogram_state.state.y

        self.dx *= (self.widget_width_px / float(x))
        self.dy *= (self.widget_height_px / float(y))

    def start_search(self):
        """ Start the search in the worker thread """
        self.status_message.emit(str('Search started'))
        search = NonogramBfs(self.nonogram_state.state, self)
        self.thread.search(search)

    def set_solution(self, solution):
        """ Receives a solution from search and sets the node """
        self.nonogram_state = NonogramState(
            solution.state,
            None,
            solution.domains,
            solution.solution_length
        )

    def paint(self, state):
        """ Receives a node and tells Qt to update the graphics """
        self.nonogram_state = state

        self.update()

    def paintEvent(self, _): # pylint: disable=invalid-name
        """ Called by the Qt event loop when the widget should be updated """
        painter = QtGui.QPainter(self)
        self.draw_nonogram(painter)

    def resizeEvent(self, e): # pylint: disable=invalid-name
        """ Handles widget resize and scales Nonogram """
        self.widget_width_px = e.size().width()
        self.widget_height_px = e.size().height()
        self.compute_tile_size()

    def draw_nonogram(self, painter):
        """ Draws a Nonogram, WHITE should be treated as an error. """
        colors = {
            C.colors.GREY: QtGui.QColor(130, 130, 130), # Unset
            C.colors.PINK: QtGui.QColor(255, 255, 150), # Drawn
            C.colors.YELLOW: QtGui.QColor(255, 0, 150), # Space
            C.colors.WHITE: QtGui.QColor(255, 255, 255) # No domains
        }

        for y, row in enumerate(self.nonogram_state.representation()):
            for x, element in enumerate(row):
                painter.setBrush(colors[int(element)])
                painter.drawRect(x*self.dx, y*self.dy, self.dx - 1, self.dy - 1)

    def set_nonogram(self, default=False):
        """ Load level with a QFileDialog """
        folder = res.nonograms.__path__[0]
        if default:
            path = folder + '/nono-heart-1.txt'
        else:
            path = QtGui.QFileDialog.getOpenFileName(
                self.window(), "Nonogram Selector", folder, "Text files (*.txt)"
            )
            if not path:
                return

        nonogram_file = open(path, 'r')
        contents = [line.strip() for line in nonogram_file.read().splitlines()]

        self.level_loaded(Nonogram(contents))

        filename = path.split('/')[-1]
        title = 'Module 3 - Nonogram - {}'.format(filename)
        self.parent().setWindowTitle(title)
        self.status_message.emit(str('Loaded: {}'.format(filename)))
        self.update()

    def set_delay(self, delay):
        """ Change delay """
        self.delay = delay
        self.status_message.emit('Delay: ' + str(delay))
