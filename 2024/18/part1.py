"""
Copied from the example A* implementation,

each node on the front is prioritized according to

    f = g + h

where g is the number of steps taken so far, and h is an optimistic
estimation of the number of steps left, the heuristic.
"""

import numpy as np
from queue import PriorityQueue

# load the indices
inds = []
start = (0, 0)
target = (70, 70)
with open("input.txt", "r") as fp:
    for line in fp:
        j, i = map(int, line.strip().split(","))
        inds.append((i, j))

# fill a maze with the first 1024 blocks
field = np.zeros((71, 71), dtype=int)
for i in range(1024):
    field[inds[i][0], inds[i][1]] = 1

def h(node):
    # Manhattan heuristic
    return abs(target[1] - node[1]) + abs(target[0] - node[0])

def find_neighbors(pos):
    found = []
    for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ind = (pos[0] + d[0], pos[1] + d[1])
        if min(ind) < 0 or max(ind) >= field.shape[0]:
            continue
        if field[ind[0]][ind[1]] == 0:
            found.append(ind)
    return found

q = PriorityQueue()
q.put((0 + h(start), start, []))  # use (priority, pos, history) tuples

visited = set()
while q.qsize():
    # pick a node to move forward!
    f, node, history = q.get(timeout=0)  # will fail if empty

    # see if we're finished
    if node == target:
        print(f"Got there in {f} steps")
        break

    # find the neighbors and update their f values
    neighbors = find_neighbors(node)
    g = f - h(node)  # path taken so far
    for n_ in neighbors:
        if n_ in visited:
            continue

        f = g + 1 + h(n_)
        q.put((f, n_, history+[node,]))
        visited.add(n_)

assert f == 408

## visualize
import matplotlib.pyplot as plt; plt.ion()
import numpy as np
board = np.array([[c == 1 for c in row] for row in field], dtype=int)
for his in history:
    board[his] = 2
board[start] = 3
board[target] = 3
plt.imshow(board)