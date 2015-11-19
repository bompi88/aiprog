import pickle

import res.play2048s

filename = '1447941815.p'

f = open(res.play2048s.__path__[0] + '/' + filename, 'rb')

states = pickle.load(f)

for states in states:
    print(states[0], end=' => ')
    print(states[1])
