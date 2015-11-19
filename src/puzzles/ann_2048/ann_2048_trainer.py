from src.algorithms.ann.sum_of_squared_errors import SumOfSquaredErrors
from src.algorithms.ann.ann import Ann
from src.utils.ann2048_basics import load_2048_example
from theano import tensor as T


class Ann2048Trainer(object):
    def __init__(self, gui_worker=None):

        print('----> Loading cases...')

        training_set = load_2048_example()
        testing_set = load_2048_example()

        provided_datasets = [
            training_set,
            testing_set
        ]

        self.net = Ann(
            structure=[16, 200, 4],
            datasets=provided_datasets,
            activation_function=[T.nnet.sigmoid, T.nnet.sigmoid],
            learning_rate=0.1,
            regression_layer=SumOfSquaredErrors
        )

        self.gui_worker = gui_worker

    def train(self, epochs=60):
        self.net.train(epochs)

    # def test(self):
    #    minor_demo(self.net)

if __name__ == '__main__':

    trainer = Ann2048Trainer()

    trainer.train()
    # trainer.test()
