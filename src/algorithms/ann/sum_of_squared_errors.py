from src.algorithms.ann.logistic_regression_layer import LogisticRegressionLayer
import theano.tensor as T


class SumOfSquaredErrors(LogisticRegressionLayer):

    def __init__(self, _input, n_in, n_out, activation=T.nnet.sigmoid):
        LogisticRegressionLayer.__init__(self, _input, n_in, n_out, activation)

    def error(self, label):
        return T.sum((self.prediction - label)**2)
