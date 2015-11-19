from PyQt4.QtCore import QThread

from src.puzzles.mnist.mnist_trainer import MNISTTrainer


class MNISTWorker(QThread):
    """ Inherit QThread for easy threading """

    def __init__(self, gui):
        QThread.__init__(self, None)
        self.exiting = False

        self.gui = gui
        self.trainer = MNISTTrainer

    def run(self):
        self.trainer = self.trainer(self)
        self.trainer.train()
        self.trainer.test()

        self.gui.ended()

    def train(self):
        self.trainer.train()

        self.gui.ended()

    def test(self):
        self.trainer.test()

        self.gui.ended()

    def end_worker(self):
        self.setTerminationEnabled(True)
        self.terminate()
        self.gui.status_message.emit('Terminated')

    def plot(self, data):
        self.gui.new_data.emit(data)

    def __del__(self):
        self.exiting = True
        self.wait()
