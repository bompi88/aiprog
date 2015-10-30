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
        self.predictor = None
        self.trainer = None

        self.construct_net()

    def construct_net(self):
        pass

    def update_net(self, case):
        return 0

    def predict(self, case):
        return 0

    def train(self, cases, epochs=100):
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

    def test(self, cases):
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
