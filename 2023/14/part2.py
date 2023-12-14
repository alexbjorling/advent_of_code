import numpy as np
import re
from functools import lru_cache

with open('input.txt', 'r') as fp:
    text = fp.read().replace('\n', '')

# load into a numpy array so we can handle columns more easily
N = int(np.sqrt(len(text)))
data = np.copy(np.frombuffer(text.encode(), dtype=np.uint8).reshape((N, -1)))

# helper function to push balls as far left as possible in a string
@lru_cache(maxsize=None)
def push_left(txt):
    for match in re.finditer('([.O]+)', txt):
        start, end = match.span()
        n_balls = txt[start:end].count('O')
        n_dots = txt[start:end].count('.')
        txt = txt[:start] + n_balls * 'O' + n_dots * '.' + txt[end:]
    return txt

# go over all the columns as text, pushing the balls north
record = np.zeros((10000, N, N), dtype=np.uint8)
for cycle in range(1000000000):
    if cycle % 100 == 0:
        print(cycle)

    # roll north
    for col in data.T:
        txt = push_left(col.tobytes().decode())
        col[:] = np.frombuffer(txt.encode(), dtype=np.uint8)

    # roll west
    for row in data:
        txt = push_left(row.tobytes().decode())
        row[:] = np.frombuffer(txt.encode(), dtype=np.uint8)

    # roll south
    for col in data.T:
        txt = push_left(col.tobytes().decode()[::-1])[::-1]
        col[:] = np.frombuffer(txt.encode(), dtype=np.uint8)

    # roll east
    for row in data:
        txt = push_left(row.tobytes().decode()[::-1])[::-1]
        row[:] = np.frombuffer(txt.encode(), dtype=np.uint8)

    # look for repetition
    matches = np.prod((record[:cycle+1] == data), axis=-1)
    if matches.any():
        print('match!', np.where(matches))
    record[cycle] == data


# sum up the weights
ballchar = np.frombuffer(b'O', dtype=np.uint8)[0]
rocks = (data == ballchar).astype(int)
weights = np.arange(N, 0, -1).reshape((N, -1))

print(np.sum(rocks * weights))
