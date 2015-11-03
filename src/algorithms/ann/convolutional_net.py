"""
Defines a neural net.
"""

from src.utils.preprocessing import preprocess
from src.algorithms.ann.convolutional_layer import ConvolutionalLayer
from src.algorithms.ann.hidden_layer import HiddenLayer
from src.algorithms.ann.logistic_regression_layer import LogisticRegressionLayer

from theano import tensor as T
import theano
import numpy


class ConvolutionalNet(object):

    def __init__(self, structure, learning_rate=0.1, batch_size=20):
        """
        Creates a convolutional neural net.

        :param structure: list of number of nodes per layer: [inputLayer, hiddenLayers... , outputLayer]
        :param activation_functions: 'sigmoid', 'tanh' etc for each layer except the output layer ['sigmoid', 'tanh' ...]
        :param learning_rate: learing rate at each layer except output layer
        :return:
        """

        self.random_feed = numpy.random.RandomState(23455)

        self.structure = structure
        self.learning_rate = learning_rate
        self.batch_size = batch_size

        # Our Theano functions
        self.tester = None
        self.validator = None
        self.trainer = None

        self.x = None
        self.y = None
        self.cost = None
        self.index = 0
        self.params = []
        self.updates = None
        self.gradients = None

        self.layers = []

        self.test_set_x = None
        self.test_set_y = None

        self.train_set_x = None
        self.train_set_y = None

        self.valid_set_x = None
        self.valid_set_y = None

        self.construct_net()

    def construct_net(self):
        print('----> Constructing the neural net...')

        self.index = T.lscalar()
        x = T.matrix('x')   # images
        y = T.ivector('y')  # labels

        input_to_first_layer = x.reshape((self.batch_size, 1, 28, 28))

        input_to_next_layer = None

        for idx, layer_def in enumerate(self.structure):

            if layer_def['type'] == 'convolution':
                self.layers.append(
                    ConvolutionalLayer(
                        self.random_feed,
                        _input=input_to_next_layer if len(self.layers) else input_to_first_layer,
                        image_shape=(
                            self.batch_size,
                            self.structure[idx-1]['number_of_kernels'] if len(self.layers) else 1,
                            layer_def['image_size'][0],
                            layer_def['image_size'][1]
                        ),
                        filter_shape=(
                            layer_def['number_of_kernels'],
                            self.structure[idx-1]['number_of_kernels'] if len(self.layers) else 1,
                            layer_def['filter_size'][0],
                            layer_def['filter_size'][1]
                        ),
                        poolsize=layer_def['pool_size']
                    )
                )
            elif layer_def['type'] == 'hidden':
                if self.structure[idx-1]['type'] == 'convolution':
                    self.layers.append(
                        HiddenLayer(
                            self.random_feed,
                            _input=input_to_next_layer.flatten(2),
                            n_in=self.structure[idx-1]['number_of_kernels'] * 4 * 4,
                            n_out=layer_def['output_size'],
                            activation=layer_def['activation_function']
                        )
                    )
                else:
                    self.layers.append(
                        HiddenLayer(
                            self.random_feed,
                            _input=input_to_next_layer,
                            n_in=self.structure[idx-1]['output_size'],
                            n_out=layer_def['output_size'],
                            activation=layer_def['activation_function']
                        )
                    )
            elif layer_def['type'] == 'logistic_regression':
                self.layers.append(
                    LogisticRegressionLayer(
                        _input=input_to_next_layer,
                        n_in=self.structure[idx-1]['output_size'],
                        n_out=layer_def['output_size']
                    )
                )

            input_to_next_layer = self.layers[idx].output

        self.cost = self.layers[-1].negative_log_likelihood(y)

        for layer in self.layers:
            self.params += layer.params

        self.gradients = T.grad(self.cost, self.params)

        self.updates = [
            (param_i, param_i - self.learning_rate * grad_i)
            for param_i, grad_i in zip(self.params, self.gradients)
        ]

    def update_net(self, case):
        return 0

    def predict(self, case):
        return 0

    def train(self, train_set_x, train_set_y, epochs=100):
        print('----> Started training...')

        self.train_set_x = train_set_x
        self.train_set_y = train_set_y

        if self.trainer is None:
            self.trainer = theano.function(
                [self.index],
                self.cost,
                updates=self.updates,
                givens={
                    self.x: self.train_set_x[self.index * self.batch_size: (self.index + 1) * self.batch_size],
                    self.y: self.train_set_y[self.index * self.batch_size: (self.index + 1) * self.batch_size]
                }
            )

        epoch = 0
        errors = []

        while epoch < epochs:
            epoch += 1
            error = 0

            for case in cases:
                preprocessed_case = preprocess(case)
                error += self.update_net(preprocessed_case)

            errors.append(error)

        return errors

    def validate(self, valid_set_x, valid_set_y):
        print('----> Started validation...')

        self.valid_set_x = valid_set_x
        self.valid_set_y = valid_set_y

        if self.validator is None:
            self.validator = theano.function(
                [self.index],
                self.layers[-1].errors(self.y),
                givens={
                    self.x: self.valid_set_x[self.index * self.batch_size: (self.index + 1) * self.batch_size],
                    self.y: self.valid_set_y[self.index * self.batch_size: (self.index + 1) * self.batch_size]
                }
            )

    def test(self, test_set_x, test_set_y):
        print('----> Started testing...')

        self.test_set_x = test_set_x
        self.test_set_y = test_set_y

        if self.tester is None:
            self.tester = theano.function(
                [self.index],
                self.layers[-1].errors(self.y),
                givens={
                    self.x: self.test_set_x[self.index * self.batch_size: (self.index + 1) * self.batch_size],
                    self.y: self.test_set_y[self.index * self.batch_size: (self.index + 1) * self.batch_size]
                }
            )

        predictions = []
        for case in cases:
            # Preprocess the features before running the Ann
            preprocessed_case = preprocess(case)

            # Predict using Ann
            prediction = self.predict(preprocessed_case)

            # Add prediciton to predictions list
            predictions.append(prediction)
        return predictions

    def blind_test(self, cases):
        """
        This method should predict a value for all testobjects in the list feature_sets, and return a list with the
        predictions.
        :param feature_sets: list of sublists, where the sublists are the images to classify.
        :return:
        """
        return self.test(cases)

if __name__ == '__main__':

    net_structure = [
        {
            'type': 'convolution',
            'number_of_kernels': 20,
            'pool_size': (2, 2),
            'image_size': (28, 28),
            'filter_size': (5, 5)
        },
        {
            'type': 'convolution',
            'number_of_kernels': 50,
            'pool_size': (2, 2),
            'image_size': (12, 12),
            'filter_size': (5, 5)
        },
        {
            'type': 'hidden',
            'output_size': 500,
            'activation_function': T.tanh
        },
        {
            'type': 'logistic_regression',
            'output_size': 10
        }
    ]

    net = ConvolutionalNet(net_structure, 0.1, 500)
