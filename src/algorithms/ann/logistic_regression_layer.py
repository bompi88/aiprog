import theano.tensor as T
import theano
import numpy


class LogisticRegressionLayer(object):

    def __init__(self, _input, n_in, n_out, activation=T.nnet.sigmoid):

        self.input = _input

        self.w = theano.shared(
            value=numpy.zeros(
                (n_in, n_out),
                dtype=theano.config.floatX
            ),
            name='w',
            borrow=True
        )

        self.b = theano.shared(
            value=numpy.zeros(
                (n_out,),
                dtype=theano.config.floatX
            ),
            name='b',
            borrow=True
        )

        self.prediction = activation(T.dot(_input, self.w) + self.b)
        self.params = [self.w, self.b]

    def error(self, label):
        """ Backpropagation error calculation """
        raise NotImplementedError(
            'Implement error() in LogisticRegressionLayer subclass')