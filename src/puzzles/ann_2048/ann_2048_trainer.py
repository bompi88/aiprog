from src.utils.ann2048_basics import process_states
from src.algorithms.ann.ann import Ann
from src.utils.ann2048_basics import load_2048_example
from theano import tensor as T
import res.play2048s.anns
import pickle


class Ann2048Trainer(object):
    def __init__(self, structure=None, provided_datasets=None,
                 activation_function=None, regression_layer=None,
                 learning_rate=None, gui_worker=None):

        if not provided_datasets:
            min_tile = None
            heuristic = None
            num_cases = None

            if gui_worker:
                min_tile = gui_worker.gui.min_save_tiles
                heuristic = gui_worker.gui.heuristic
                num_cases = gui_worker.gui.num_cases
            else:
                print('----> Loading cases...')

            training_set = load_2048_example(min_tile, heuristic, num_cases)
            testing_set = load_2048_example(min_tile, heuristic, num_cases)

            provided_datasets = [
                training_set,
                testing_set
            ]

        self.net = Ann(
            gui_worker=gui_worker,
            structure=structure if structure else [17, 300, 60, 4],
            datasets=provided_datasets,
            activation_function=activation_function if activation_function else [T.nnet.sigmoid, T.nnet.sigmoid, T.nnet.sigmoid, T.nnet.sigmoid, T.nnet.sigmoid],
            learning_rate=learning_rate,
            regression_layer=regression_layer,
            normalize=process_states
        )

        self.gui_worker = gui_worker

    def save(self, path=None):
        if not path:
            path = res.play2048s.anns.__path__[0] + "/trained-ann-2048"

        file = open(path, 'wb')
        pickle.dump(self.net, file, protocol=pickle.HIGHEST_PROTOCOL)
        file.close()

    def train(self, epochs=100):
        self.net.train(epochs)

if __name__ == '__main__':

    trainer = Ann2048Trainer()

    trainer.train(100)
    trainer.save()
