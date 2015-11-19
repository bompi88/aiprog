import res.play2048s.manual_upper_left_focus.max_2048
import pickle


def load_2048_example():
    path = res.play2048s.manual_upper_left_focus.max_2048.__path__[0]
    file_path = path + '/' + '1447943503.p'
    f = open(file_path, 'rb')
    data = pickle.load(f)

    features, labels = [], []

    for line in data:
        features.append(line[1])
        labels.append(line[0])

    return features, labels
w