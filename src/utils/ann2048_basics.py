import res.play2048s.ai_runs
import pickle
import numpy as np
from copy import deepcopy
import random


def load_2048_example(min_tile, heuristic, cases):
    path = res.play2048s.ai_runs.__path__[0]
    data = {}

    min_tile = min_tile if min_tile else 1
    heuristic = heuristic if heuristic else 0
    cases = cases if cases else 30000

    while min_tile < 15:
        file_path = path + '/' + str(2 ** min_tile) + '_' + str(heuristic) + '.p'

        try:
            f = open(file_path, 'rb')
        except FileNotFoundError:
            min_tile += 1
            continue
        while 1:
            try:
                z = data.copy()
                z.update(pickle.load(f))
                data = z
            except EOFError:
                break
        min_tile += 1

    features, labels = [], []

    for line in list(data.values())[:cases]:
        features.append(process(line[1]))
        labels.append(line[0])

    return (features[:int(cases*0.9)], labels[:int(cases*0.9)]), (features[int(cases*0.9):], labels[int(cases*0.9):])


def eightway_mirror(states):
    return_states = []

    for state in states:
        label = state[0]
        feature = state[1]

        mirrored = list_mirror(feature)

        for new_feature in mirrored:
            return_states.append((label, new_feature))

    return return_states


def list_mirror(feature):
    eight_states = []

    np_arr = np.array(feature)

    np_matrix = np_arr.reshape((4, 4))
    flipped = np.fliplr(np_matrix)

    eight_states.append(list(np_arr))
    eight_states.append(list(flipped.reshape(16)))

    for rot in range(1, 4):
        eight_states.append(list(np.rot90(np_matrix, rot).reshape(16)))
        eight_states.append(list(np.rot90(flipped, rot).reshape(16)))

    return eight_states


def process_states(states):
    r = []
    for state in states:
        r.append(process(deepcopy(state)))
    return r


def process(state):

    modifier = [
        15, 14, 13, 12,
        8, 9, 10, 11,
        7, 6, 5, 4,
        0, 1, 2, 3
    ]

    sub = 15 - max(state)

    sum = 0

    for i in range(16):

        if modifier[i] - sub >= 0:
            modifier[i] = sub - modifier[i]

        if state[i] != 0:
            # state[i] = (modifier[i] + state[i]) # * state[i] # * (16 - modifier[i])
            state[i] = (modifier[i] + state[i]) #  * state[i] # * state[i] * (16 - modifier[i])
        sum += abs(state[i])

    # state = [s / (1 + max(state)) for s in state]
    #
    if len(state) == 16:
        state.append(max(state))
    #     state.append(sum)
    return state
