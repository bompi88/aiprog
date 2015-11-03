import theano.tensor as T
import theano
import numpy


class HiddenLayer(object):

    def __init__(self, rng, _input, n_in, n_out, w=None, b=None, activation=T.tanh):
        self.input = _input

        if w is None:
            w_values = numpy.asarray(
                rng.uniform(
                    low=-numpy.sqrt(6. / (n_in + n_out)),
                    high=numpy.sqrt(6. / (n_in + n_out)),
                    size=(n_in, n_out)
                ),
                dtype=theano.config.floatX
            )
            if activation == theano.tensor.nnet.sigmoid:
                w_values *= 4

            w = theano.shared(value=w_values, name='w', borrow=True)

        if b is None:
            b_values = numpy.zeros((n_out,), dtype=theano.config.floatX)
            b = theano.shared(value=b_values, name='b', borrow=True)

        self.w = w
        self.b = b

        lin_output = T.dot(_input, self.w) + self.b
        self.output = (
            lin_output if activation is None
            else activation(lin_output)
        )

        self.params = [self.w, self.b]
