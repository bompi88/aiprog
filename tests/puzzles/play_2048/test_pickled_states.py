import pickle
from src.utils.ann2048_basics import eightway_mirror

import res.play2048s

filename = '1447966849.p'

f = open(res.play2048s.__path__[0] + '/' + filename, 'rb')

states = pickle.load(f)

for i, state in enumerate(eightway_mirror(states)):
    print(i, end=': ')
    print(state[0], end=' => ')
    print(state[1])
