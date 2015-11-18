""" A Widget for drawing Graph states """
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal

from src.modules.module5.utils.mnist_worker import MNISTWorker


class MNISTGUI(QtGui.QFrame):
    """ Implement QFrame, which is a subclass of QWidget """
    status_message = pyqtSignal(str)
    score_message = pyqtSignal(str)

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)

        self.worker = None
        self.started = False

        self.widget_size_px = 600
        self.init_ui()

    def init_ui(self):
        """ Initialize the UI """
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        size = QtCore.QSize(self.widget_size_px, self.widget_size_px)
        self.setMinimumSize(size)
        self.parent().adjustSize()
        self.parent().setWindowTitle('Module 5 - MNIST classification')

    def start_training(self):
        """ Start the search in the worker thread """
        self.end()
        self.train()

    def ended(self):
        self.status_message.emit('Terminated..')

    def start_manual_game(self):
        self.start(True)

    def end(self):
        if not self.started:
            return

        self.worker.end_worker()
        self.worker = None
        self.started = False

    def train(self):
        if self.started:
            return

        self.worker = MNISTWorker(self)
        self.worker.train()

        self.started = True
        self.update()

        self.status_message.emit(str('Training started...'))

    def test(self):
        if self.started:
            return

        if not self.worker:
            self.status_message.emit(str('Train first...'))
            return

        self.worker.test()

        self.started = True
        self.update()

        self.status_message.emit(str('Testing started...'))

    def paintEvent(self, _):  # pylint: disable=invalid-name
        """ Called by the Qt event loop when the widget should be updated """
        painter = QtGui.QPainter(self)

        # self.paint_image(painter, image)

    def resizeEvent(self, e):  # pylint: disable=invalid-name
        """ Handles widget resize """
        size = max(e.size().width(), e.size().height())
        self.setMinimumSize(QtCore.QSize(size, size))
        self.widget_size_px = size

    def reset_size(self):
        self.widget_size_px = 600
        self.setMinimumSize(QtCore.QSize(self.widget_size_px,
                                         self.widget_size_px))
        self.parent().adjustSize()
        self.update()

    def paint_image(self, painter, image):
        """ Draws an MNIST image """
        return
