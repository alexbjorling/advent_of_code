"""
Method: draw a vertical line from each point to infinity. If it meets parts
of the loop with a horizontal component an odd number of times, it's inside.
"""

import numpy as np

# the pipes operate on a direction vector (di, dj) as follows
identity = np.identity(2, dtype=int)
switch = (1 - identity)
operator = {
    '-': identity,
    '|': identity,
    '7': switch,
    'L': switch,
    'J': -switch,
    'F': -switch,
}

# load data and find the starting position
i0, j0 = None, None
with open('input.txt', 'r') as fp:
    data = fp.read().strip().split('\n')
for ii in range(len(data)):
    if 'S' in data[ii]:
        i0 = ii
        j0 = data[ii].index('S')
assert None not in (i0, j0)
i, j = i0, j0

# look for the two connections available, and pick a starting direction
connections = []
if (i > 0) and (data[i - 1][j] in '7F|'):
    connections.append((-1, 0))
if (i < len(data) - 1) and (data[i + 1][j] in 'JL|'):
    connections.append((1, 0))
if  (j > 0) and (data[i][j - 1] in 'FL-'):
    connections.append((0, -1))
if (j < len(data[0]) - 1) and (data[i][j + 1] in 'J7-'):
    connections.append((0, 1))
direction = connections[0]

# determine and replace the pipe under S for later
if (1, 0) in connections and (-1, 0) in connections:
    S = '|'
elif (1, 0) in connections and (0, -1) in connections:
    S = '7'
elif (1, 0) in connections and (0, 1) in connections:
    S = 'F'
elif (-1, 0) in connections and (0, 1) in connections:
    S = 'L'
elif (-1, 0) in connections and (0, -1) in connections:
    S = 'J'
elif (0, 1) in connections and (0, -1) in connections:
    S = '-'
data[i0] = data[i0].replace('S', S)

# go around the loop to map it out
loop = []
i, j = i0, j0
while (i, j) != (i0, j0) or not loop:
    loop.append((i, j))
    i += direction[0]
    j += direction[1]
    direction = np.dot(operator[data[i][j]], direction)

# make an outline of the loop border for faster checking
M, N = len(data), len(data[0])
outline = np.zeros((M, N), dtype=bool)
for ll in loop:
    m, n = ll
    outline[m, n] = True

# count the number of points inside the loop by the above method
total = 0
for ii in range(M):
    for jj in range(N):
        if outline[ii, jj]:
            continue
        crossings = 0
        last_bend = ''
        for di in range(M - ii):
            if not outline[ii + di, jj]:
                continue
            pipe = data[ii + di][jj]
            if pipe == '-':
                crossings += 1
            elif pipe in '7F':
                last_bend = pipe
            elif (pipe == 'L' and last_bend == '7') or (pipe == 'J' and last_bend == 'F'):
                crossings += 1
        if crossings % 2:
            total += 1

assert total == 567
