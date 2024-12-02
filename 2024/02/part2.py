import numpy as np

def safe(arr):
    incr = np.all(np.diff(arr) > 0)
    decr = np.all(np.diff(arr) < 0)
    max_3 = np.max(np.abs(np.diff(arr))) <= 3
    if (incr or decr) and max_3:
        return True
    else:
        return False

tot = 0
with open('input.txt', 'r') as fp:
    for line in fp:
        line = list(map(int, line.split()))
        if safe(line):
            tot += 1
        else:
            for i in range(len(line)):
                if safe(line[:i] + line[i+1:]):
                    tot += 1
                    break

assert tot == 569