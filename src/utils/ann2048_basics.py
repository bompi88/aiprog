import res.play2048s.manual_upper_left_focus.max_2048
import pickle


def load_2048_example():
    path = res.play2048s.manual_upper_left_focus.max_2048.__path__[0]
    file_path = path + '/' + '1447943503.p'
    f = open(file_path, 'rb')
    data = pickle.load(f)

    features, labels = [], []

    for line in data:
        features.append(process(line[1]))
        labels.append(line[0])

    return features, labels


def process_states(states):
    for state in states:
        process(state)

    return states


def process(state):
    modifier = [
        15, 14, 13, 12,
        8, 9, 10, 11,
        7, 6, 5, 4,
        0, 1, 2, 3
    ]

    sub = 15 - max(state)

    for i, tile in enumerate(state):

        if modifier[i] - sub >= 0:
            modifier[i] = sub - modifier[i]

        if state[i] != 0:
            state[i] = (modifier[i] + state[i]) * state[i] # * (16 - modifier[i])

    return state
