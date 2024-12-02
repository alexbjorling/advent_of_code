import numpy as np

tot = 0
with open('input.txt', 'r') as fp:
    for line in fp:
        line = np.array(list(map(int, line.split())))
        incr = np.all(np.diff(line) > 0)
        decr = np.all(np.diff(line) < 0)
        max_3 = np.max(np.abs(np.diff(line))) <= 3

        if (incr or decr) and max_3:
            tot += 1

assert tot == 524