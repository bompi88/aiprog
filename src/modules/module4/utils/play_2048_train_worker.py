from PyQt4.QtCore import QThread

from src.puzzles.ann_2048.ann_2048_trainer import Ann2048Trainer


class Play2048TrainWorker(QThread):
    """ Inherit QThread for easy threading """

    def __init__(self, gui, structure=None, provided_datasets=None, activation_function=None, regression_layer=None,
                 learning_rate=None):
        QThread.__init__(self, None)
        self.exiting = False

        self.gui = gui
        self.trainer = Ann2048Trainer(
            gui_worker=self,
            structure=structure,
            provided_datasets=provided_datasets,
            activation_function=activation_function,
            regression_layer=regression_layer,
            learning_rate=learning_rate
        )

    def run(self):
        self.trainer.train()
        self.trainer.save()
        self.gui.training_ended()

    def end_worker(self):
        self.setTerminationEnabled(True)
        self.terminate()
        self.gui.status_message.emit('Training terminated')

    def __del__(self):
        self.exiting = True
        self.wait()
