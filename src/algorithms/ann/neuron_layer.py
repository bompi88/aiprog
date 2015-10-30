from theano import tensor as T


class NeuronLayer(object):

    def __init__(self, input, n_input, n_output, w=None, b=None, activation_function=T.sigmoid):
        """

        :param input:
        :param n_input:
        :param n_output:
        :param W:
        :param b:
        :param activation_function:
        :return:
        """
        self.input = input
        self.n_input = n_input
        self.n_output = n_output
        self.w = w
        self.b = b
        self.activation_function = activation_function

        # weight = theano.shared(np.random.uniform(-0.1, 0.1, size=(self.structure[idx], self.structure[idx + 1])))