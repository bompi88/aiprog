from theano.tensor.signal import downsample
from theano.tensor.nnet import conv
import theano.tensor as T
import theano
import numpy


class ConvolutionalLayer(object):

    def __init__(self, rng, _input, filter_shape, image_shape, poolsize=(2, 2)):

        assert image_shape[1] == filter_shape[1]
        self.input = _input

        fan_in = numpy.prod(filter_shape[1:])
        fan_out = (filter_shape[0] * numpy.prod(filter_shape[2:]) /
                   numpy.prod(poolsize))

        w_bound = numpy.sqrt(6. / (fan_in + fan_out))
        self.w = theano.shared(
            numpy.asarray(
                rng.uniform(low=-w_bound, high=w_bound, size=filter_shape),
                dtype=theano.config.floatX
            ),
            borrow=True
        )

        b_values = numpy.zeros((filter_shape[0],), dtype=theano.config.floatX)
        self.b = theano.shared(value=b_values, borrow=True)

        conv_out = conv.conv2d(
            input=_input,
            filters=self.w,
            filter_shape=filter_shape,
            image_shape=image_shape
        )

        pooled_out = downsample.max_pool_2d(
            input=conv_out,
            ds=poolsize,
            ignore_border=True
        )

        self.output = T.tanh(pooled_out + self.b.dimshuffle('x', 0, 'x', 'x'))

        self.params = [self.w, self.b]
