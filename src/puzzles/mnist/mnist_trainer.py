from src.algorithms.ann.sum_of_squared_errors import SumOfSquaredErrors
from src.utils.mnist_basics import load_all_flat_cases, minor_demo
from src.algorithms.ann.ann import Ann
from theano import tensor as T


class MNISTTrainer(object):
    def __init__(self, gui_worker=None):

        print('----> Loading cases...')

        training_set = load_all_flat_cases('training')
        testing_set = load_all_flat_cases('testing')

        provided_datasets = [
            training_set,
            testing_set
        ]

        self.net = Ann(
            structure=[784, 50, 30, 10],
            datasets=provided_datasets,
            activation_function=[T.nnet.sigmoid, T.nnet.sigmoid, T.nnet.sigmoid],
            learning_rate=0.1,
            regression_layer=SumOfSquaredErrors,
            gui_worker=gui_worker
        )

        self.gui_worker = gui_worker

    def train(self, epochs=60):
        self.net.train(epochs)

    def test(self):
        minor_demo(self.net)

if __name__ == '__main__':

    trainer = MNISTTrainer()

    trainer.train()
    trainer.test()
