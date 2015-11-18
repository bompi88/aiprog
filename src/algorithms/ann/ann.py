"""
Defines a neural net.
"""

from src.utils.preprocessing import normalize_images, as_binary_vector
from src.algorithms.ann.hidden_layer import HiddenLayer
from src.algorithms.ann.logistic_regression_layer import LogisticRegressionLayer
from src.utils.mnist_basics import load_all_flat_cases

from theano import tensor as T
import theano
import numpy
import time


class Ann(object):

    def __init__(self, structure, datasets, activation_function=T.nnet.sigmoid, learning_rate=0.1,
                 regression_layer=LogisticRegressionLayer):
        """
        Creates a neural net.

        :param structure: list of number of nodes per layer: [inputLayer, hiddenLayers... , outputLayer]
        :param datasets: training and test sets as list [training set, test set]
        :param activation_function: e.g. T.nnet.sigmoid
        :param learning_rate: learing rate at each layer except output layer
        :return:
        """

        self.random_feed = numpy.random.RandomState(23455)

        self.learning_rate = learning_rate
        self.activation_function = activation_function

        self.layers = []
        self.params = []
        self.labels = []

        self.train_set_images, self.train_set_labels = datasets[0]
        self.test_set_images, self.test_set_labels = datasets[1]

        print('----> Normalizing images...')

        self.train_set_images = normalize_images(self.train_set_images)
        self.test_set_images = normalize_images(self.test_set_images)

        print('----> Constructing the neural net...')

        self.input = T.dvector('input')
        self.label = T.dvector('label')

        input_to_next_layer = self.input

        # Create the layers
        for i in range(len(structure) - 1):
            a = self.activation_function[i] if type(self.activation_function) is list else self.activation_function
            if i < len(structure) - 2:
                self.layers.append(
                    HiddenLayer(
                        self.random_feed,
                        _input=input_to_next_layer,
                        n_in=structure[i],
                        n_out=structure[i+1],
                        activation=a
                    )
                )
                input_to_next_layer = self.layers[i].output
            else:
                # create last layer
                self.layers.append(
                    regression_layer(
                        _input=input_to_next_layer,
                        n_in=structure[i],
                        n_out=structure[i+1],
                        activation=a
                    )
                )

        self.error = self.layers[-1].error(self.label)

        for layer in self.layers:
            self.params += layer.params

        self.gradients = T.grad(self.error, self.params)

        self.updates = [
            (param, param - self.learning_rate * grad)
            for param, grad in zip(self.params, self.gradients)
        ]

        self.predictor = theano.function(
            [self.input],
            self.layers[-1].prediction
        )

        self.trainer = theano.function(
            [self.input, self.label],
            [self.layers[-1].prediction, self.error],
            updates=self.updates
        )

    def train(self, epochs=100):
        print('----> Started training...')
        errors = []
        start_time = time.time()

        for epoch in range(epochs):
            print("## Epoch ", epoch, " ##")
            n_errors = 0
            total_error = 0

            for i, c in enumerate(self.train_set_images):
                prediction, error = self.trainer(c, as_binary_vector(self.train_set_labels[i]))

                if prediction.tolist().index(max(prediction)) != self.train_set_labels[i]:
                    n_errors += 1
                total_error += error
            errors.append(total_error)
            print("Error measure: ", total_error)
            print("Number of misclassifications: ", n_errors, "\n")
            print("Error percentage: ", (n_errors / len(self.train_set_images)) * 100)
        print("", epochs, " epochs ran in ", time.time() - start_time, " seconds.")
        return errors

    def test(self):
        print('----> Started testing...')

        n_errors = 0
        start_time = time.time()

        for i, test_case in enumerate(self.test_set_images):
            prediction = self.predictor(test_case)

            if prediction.tolist().index(max(prediction)) != self.test_set_labels[i]:
                n_errors += 1

        print("Number of misclassifications: ", n_errors, "\n")
        print("Error percentage: ", (n_errors / len(self.test_set_images)) * 100)
        print("Tests ran in ", time.time() - start_time, " seconds.")

    def blind_test(self, feature_sets):
        """
        This method should predict a value for all testobjects in the list feature_sets, and returns a list with the
        predictions.
        :param feature_sets: list of sub-lists, where the sub-lists are the images to classify.
        :return:
        """
        print('----> Started blind test...')
        classifications = []

        print('----> Normalizing cases...')
        feature_sets = normalize_images(feature_sets)

        print('----> Run blind tests...')
        for test_case in feature_sets:
            prediction = self.predictor(test_case)
            classifications.append(prediction.tolist().index(max(prediction)))

        return classifications

    @staticmethod
    def print_case(case):
        for row in range(28):
            for el in case[row*28:(row+1)*28]:
                print(1 if el else 0, end="")
            print("\n", end="")


if __name__ == '__main__':

    print('----> Loading cases...')

    training_set = load_all_flat_cases('training')
    testing_set = load_all_flat_cases('testing')

    provided_datasets = [
        training_set,
        testing_set
    ]

    net = Ann(
        structure=[784, 50, 30, 10],
        datasets=provided_datasets,
        activation_function=[T.nnet.sigmoid, T.nnet.sigmoid, T.nnet.sigmoid],
        learning_rate=0.1,
        regression_layer=LogisticRegressionLayer
    )

    net.train(100)
    net.test()
