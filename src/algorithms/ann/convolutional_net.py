"""
Defines a neural net.
"""

from src.utils.preprocessing import preprocess
from src.algorithms.ann.convolutional_layer import ConvolutionalLayer
from src.algorithms.ann.hidden_layer import HiddenLayer
from src.algorithms.ann.logistic_regression_layer import LogisticRegressionLayer
from src.utils.mnist_basics import load_all_flat_cases

from theano import tensor as T
import theano
import numpy
import pickle
import os
import sys
import timeit


class ConvolutionalNet(object):

    def __init__(self, structure, datasets, learning_rate=0.1, batch_size=20):
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

        self.layers = []
        self.params = []

        self.train_set_x, self.train_set_y = datasets[0]
        self.valid_set_x, self.valid_set_y = datasets[1]
        self.test_set_x, self.test_set_y = datasets[2]

        self.n_train_batches = self.train_set_x.get_value(borrow=True).shape[0] // batch_size
        self.n_valid_batches = self.valid_set_x.get_value(borrow=True).shape[0] // batch_size
        self.n_test_batches = self.test_set_x.get_value(borrow=True).shape[0] // batch_size

        print('----> Constructing the neural net...')

        self.index = T.lscalar()
        self.x = T.matrix('x')   # images
        self.y = T.ivector('y')  # labels

        input_to_first_layer = self.x.reshape((self.batch_size, 1, 28, 28))

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
                input_to_next_layer = self.layers[idx].output
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
                input_to_next_layer = self.layers[idx].output
            elif layer_def['type'] == 'logistic_regression':
                self.layers.append(
                    LogisticRegressionLayer(
                        _input=input_to_next_layer,
                        n_in=self.structure[idx-1]['output_size'],
                        n_out=layer_def['output_size']
                    )
                )

        self.cost = self.layers[-1].negative_log_likelihood(self.y)

        for layer in self.layers:
            self.params += layer.params

        self.gradients = T.grad(self.cost, self.params)

        self.updates = [
            (param_i, param_i - self.learning_rate * grad_i)
            for param_i, grad_i in zip(self.params, self.gradients)
        ]

        self.trainer = theano.function(
            [self.index],
            self.cost,
            updates=self.updates,
            givens={
                self.x: self.train_set_x[self.index * self.batch_size: (self.index + 1) * self.batch_size],
                self.y: self.train_set_y[self.index * self.batch_size: (self.index + 1) * self.batch_size]
            }
        )

        self.validator = theano.function(
            [self.index],
            self.layers[-1].errors(self.y),
            givens={
                self.x: self.valid_set_x[self.index * self.batch_size: (self.index + 1) * self.batch_size],
                self.y: self.valid_set_y[self.index * self.batch_size: (self.index + 1) * self.batch_size]
            }
        )

        self.tester = theano.function(
            [self.index],
            self.layers[-1].errors(self.y),
            givens={
                self.x: self.test_set_x[self.index * self.batch_size: (self.index + 1) * self.batch_size],
                self.y: self.test_set_y[self.index * self.batch_size: (self.index + 1) * self.batch_size]
            }
        )

        self.predictor = theano.function(
            inputs=[self.index],
            outputs=self.layers[-1].y_pred,
            givens={
                self.x: self.test_set_x[self.index * self.batch_size: (self.index + 1) * self.batch_size]
            }
        )

    def predict(self, case):
        return self.predictor(case)

    def train(self, n_epochs=100):
        print('----> Started training...')

        patience = 5000  # look as this many examples regardless
        patience_increase = 2  # wait this much longer when a new best is
                                      # found
        improvement_threshold = 0.995  # a relative improvement of this much is
                                      # considered significant
        validation_frequency = min(self.n_train_batches, patience / 2)
                                      # go through this many
                                      # minibatche before checking the network
                                      # on the validation set; in this case we
                                      # check every epoch

        best_validation_loss = numpy.inf
        test_score = 0.
        start_time = timeit.default_timer()

        done_looping = False
        epoch = 0
        while (epoch < n_epochs) and (not done_looping):
            epoch += 1
            for minibatch_index in range(self.n_train_batches):

                minibatch_avg_cost = self.trainer(minibatch_index)
                # iteration number
                iter = (epoch - 1) * self.n_train_batches + minibatch_index

                if (iter + 1) % validation_frequency == 0:
                    # compute zero-one loss on validation set
                    validation_losses = [self.validator(i)
                                         for i in range(self.n_valid_batches)]
                    this_validation_loss = numpy.mean(validation_losses)

                    print(
                        'epoch %i, minibatch %i/%i, validation error %f %%' %
                        (
                            epoch,
                            minibatch_index + 1,
                            self.n_train_batches,
                            this_validation_loss * 100.
                        )
                    )

                    # if we got the best validation score until now
                    if this_validation_loss < best_validation_loss:
                        #improve patience if loss improvement is good enough
                        if this_validation_loss < best_validation_loss *  \
                           improvement_threshold:
                            patience = max(patience, iter * patience_increase)

                        best_validation_loss = this_validation_loss
                        # test it on the test set

                        test_losses = [self.tester(i)
                                       for i in range(self.n_test_batches)]
                        test_score = numpy.mean(test_losses)

                        print(
                            (
                                '     epoch %i, minibatch %i/%i, test error of'
                                ' best model %f %%'
                            ) %
                            (
                                epoch,
                                minibatch_index + 1,
                                self.n_train_batches,
                                test_score * 100.
                            )
                        )

                        # save the best model
                        with open('best_model.pkl', 'wb') as f:
                            pickle.dump(self.layers[-1], f)

                if patience <= iter:
                    done_looping = True
                    break

        end_time = timeit.default_timer()
        print(
            (
                'Optimization complete with best validation score of %f %%,'
                'with test performance %f %%'
            )
            % (best_validation_loss * 100., test_score * 100.)
        )
        print('The code run for %d epochs, with %f epochs/sec' % (
            epoch, 1. * epoch / (end_time - start_time)))
        sys.stderr.write('The code for file ' +
                         os.path.split(__file__)[1] +
                         ' ran for %.1fs' % (end_time - start_time))

    def test(self, cases):
        print('----> Started testing...')

        errors = []
        for case in cases:
            # Preprocess the features before running the Ann
            # preprocessed_case = preprocess(case)

            # Predict using Ann
            result = self.predict(case)

            errors.append(result)

        return errors

        # errors = 0
        # for case, label in cases:
        #     # Preprocess the features before running the Ann
        #     # preprocessed_case = preprocess(case)
        #
        #     # Predict using Ann
        #     prediction = self.predict(case)
        #
        #     errors += prediction == label
        #
        # return errors

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

    def shared_dataset(data_xy, borrow=True):
        data_x, data_y = data_xy

        shared_x = theano.shared(numpy.asarray(data_x, dtype=theano.config.floatX), borrow=borrow)
        shared_y = theano.shared(numpy.asarray(data_y, dtype=theano.config.floatX), borrow=borrow)

        return shared_x, T.cast(shared_y, 'int32')

    training_set = load_all_flat_cases('training')
    testing_set = load_all_flat_cases('testing')

    datasets = [
        shared_dataset(training_set),
        shared_dataset(testing_set),
        shared_dataset(testing_set)
    ]

    net = ConvolutionalNet(net_structure, datasets, 0.1, 100)
    net.train(1)

    print(net.test([0, 12, 13, 50, 32, 14]))
