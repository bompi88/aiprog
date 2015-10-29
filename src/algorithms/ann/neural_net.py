"""
Defines a neural net.
"""

from src.utils.preprocessing import preprocess


class NeuralNet(object):

    def __init__(self, structure, activation_functions, learning_rate):
        """
        Creates a neural net.
        :param structure: list of number of nodes per layer: [inputLayer, hiddenLayers... , outputLayer]
        :param activation_functions: 'sigmoid', 'tanh' etc for each layer except the output layer ['sigmoid', 'tanh' ...]
        :param learning_rate: learing rate at each layer except output layer
        :return:
        """
        self.structure = structure
        self.activation_functions = activation_functions
        self.learning_rate = learning_rate
        self.construct_net()

    def construct_net(self):
        pass

    def blind_test(self, feature_sets):
        """
        This method should predict a value for all testobjects in the list feature_sets, and return a list with the
        predictions.
        :param feature_sets: list of sublists, where the sublists are the images to classify.
        :return:
        """

        predictions = []

        for feature in feature_sets:
            # Preprocess the features before running the Ann
            preprocessed = preprocess(feature)

            # Predict using Ann
            # Add prediciton to predictions list
            pass

        return predictions
