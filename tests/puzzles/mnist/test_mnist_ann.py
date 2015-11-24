from src.algorithms.ann.sum_of_squared_errors import SumOfSquaredErrors
from src.utils.mnist_basics import load_all_flat_cases, minor_demo
from src.algorithms.ann.ann import Ann
from theano import tensor as T

if __name__ == '__main__':
    print('----> Loading cases...')

    training_set = load_all_flat_cases('training')
    testing_set = load_all_flat_cases('testing')

    provided_datasets = [
        training_set,
        testing_set
    ]

    net1 = Ann(
        structure=[784, 150, 10],
        datasets=provided_datasets,
        activation_function=[T.nnet.sigmoid, T.nnet.sigmoid, T.nnet.sigmoid],
        learning_rate=0.1,
        regression_layer=SumOfSquaredErrors
    )

    net1.train(100)
    minor_demo(net1)

    net2 = Ann(
        structure=[784, 150, 10],
        datasets=provided_datasets,
        activation_function=[T.nnet.sigmoid, T.nnet.sigmoid, T.nnet.sigmoid],
        learning_rate=0.2,
        regression_layer=SumOfSquaredErrors
    )

    net2.train(100)
    minor_demo(net2)

    net3 = Ann(
        structure=[784, 200, 40, 10],
        datasets=provided_datasets,
        activation_function=[T.nnet.sigmoid, T.nnet.sigmoid, T.nnet.sigmoid],
        learning_rate=0.1,
        regression_layer=SumOfSquaredErrors
    )

    net3.train(100)
    minor_demo(net3)

    net4 = Ann(
        structure=[784, 40, 10],
        datasets=provided_datasets,
        activation_function=[T.nnet.sigmoid, T.nnet.sigmoid, T.nnet.sigmoid],
        learning_rate=0.1,
        regression_layer=SumOfSquaredErrors
    )

    net4.train(100)
    minor_demo(net4)

    net5 = Ann(
        structure=[784, 200, 40, 10],
        datasets=provided_datasets,
        activation_function=[T.nnet.sigmoid, T.nnet.sigmoid, T.nnet.sigmoid],
        learning_rate=0.2,
        regression_layer=SumOfSquaredErrors
    )

    net5.train(100)
    minor_demo(net5)

net2 net5 net4 net3