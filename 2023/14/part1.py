import numpy as np
import re

with open('input.txt', 'r') as fp:
    text = fp.read().replace('\n', '')

# load into a numpy array so we can handle columns more easily
N = int(np.sqrt(len(text)))
data = np.copy(np.frombuffer(text.encode(), dtype=np.uint8).reshape((N, -1)))

# go over all the columns as text, pushing the balls north
for col in data.T:
    txt = col.tobytes().decode()
    for match in re.finditer('([.O]+)', txt):
        start, end = match.span()
        n_balls = txt[start:end].count('O')
        n_dots = txt[start:end].count('.')
        txt = txt[:start] + n_balls * 'O' + n_dots * '.' + txt[end:]
    col[:] = np.frombuffer(txt.encode(), dtype=np.uint8)

# print the result for inspection?
def print_state(data):
    # print the result
    txt = data.tobytes().decode()
    split = [txt[i*N:i*N+N] for i in range(N)]
    for l in split:
        print(l)
    print()
#print_state(data)

# sum up the weights
ballchar = np.frombuffer(b'O', dtype=np.uint8)[0]
rocks = (data == ballchar).astype(int)
weights = np.arange(N, 0, -1).reshape((N, -1))

assert np.sum(rocks * weights) == 105208
