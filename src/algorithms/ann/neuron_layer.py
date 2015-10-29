class NeuronLayer(object):

    def __init__(self, input, n_input, n_output, W=None, b=None, activation_function=T.sigmoid):
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
        self.W = W
        self.b = b
        self.activation_function = activation_function


