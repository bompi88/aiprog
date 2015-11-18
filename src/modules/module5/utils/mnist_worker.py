from time import sleep
from PyQt4.QtCore import QThread

from src.puzzles.mnist.mnist_trainer import MNISTTrainer


class MNISTWorker(QThread):
    """ Inherit QThread for easy threading """

    def __init__(self, gui):
        QThread.__init__(self, None)
        self.exiting = False

        self.gui = gui
        self.trainer = MNISTTrainer(self)

    def train(self):
        self.trainer.train()

        self.gui.ended()

    def test(self):
        self.trainer.test()

        self.gui.ended()

    def move_completed(self):
        if self.gui.take_screenshots:
            self.gui.screenshot.emit()

        sleep(self.gui.delay / 1000.0)
        self.gui.score_message.emit('Score: {}'.format(self.player.game.score))
        self.gui.update()

    def end_worker(self):
        self.setTerminationEnabled(True)
        self.terminate()
        self.gui.status_message.emit('Terminated')

    def __del__(self):
        self.exiting = True
        self.wait()

    def __str__(self):
        return '\n'.join(['-'.join(str(t) for t in r) for r in self.game.board])
