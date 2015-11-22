from time import sleep
from PyQt4.QtCore import QThread

from src.puzzles.ann_2048.ann_2048_tester import Ann2048Tester


class Play2048TestWorker(QThread):
    """ Inherit QThread for easy threading """

    def __init__(self, gui, path=None, ann=None):
        QThread.__init__(self, None)
        self.exiting = False

        self.gui = gui
        self.tester = Ann2048Tester(
            gui_worker=self,
            path=path,
            ann=ann
        )

        self.states = []

    def run(self):
        self.tester.play()
        self.gui.testing_ended()

    def move_completed(self, state):
        if self.gui.take_screenshots:
            self.gui.screenshot.emit()

        sleep(self.gui.delay / 1000.0)
        self.gui.score_message.emit('Score: {}'.format(self.tester.game.score))

        self.gui.update()

    def end_worker(self):
        self.setTerminationEnabled(True)
        self.terminate()
        self.gui.status_message.emit('Testing terminated')

    def board(self):
        return self.tester.game.board

    def __del__(self):
        self.exiting = True
        self.wait()

    def __str__(self):
        return '\n'.join(['-'.join(str(t) for t in r) for r in self.board()])
