import theano.tensor as T


def sigmoid(m, threshold=0):
    x, y, b = T.dvectors('x', 'y', 'b')
    w = T.dmatrix('W')
    y = T.nnet.sigmoid(T.dot(w, x) + b)
    return y(m)


def ultra_fast_sigmoid(m, threshold=0):
    x, y, b = T.dvectors('x', 'y', 'b')
    w = T.dmatrix('W')
    y = T.nnet.ultra_fast_sigmoid(T.dot(w, x) + b)
    return y(m)


def softplus(m, threshold=0):
    x, y, b = T.dvectors('x', 'y', 'b')
    w = T.dmatrix('W')
    y = T.nnet.softplus(T.dot(w, x) + b)
    return y(m)


def softmax(m, threshold=0):
    x, y, b = T.dvectors('x', 'y', 'b')
    w = T.dmatrix('W')
    y = T.nnet.softmax(T.dot(w, x) + b)
    return y(m)


def relu(m, threshold=0):
    x, y, b = T.dvectors('x', 'y', 'b')
    w = T.dmatrix('W')
    y = T.nnet.softplus(T.dot(w, x) + b)
    return y(m, threshold)
