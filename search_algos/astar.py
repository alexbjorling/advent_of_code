"""
Example A* implementation,

each node on the front is prioritized according to

    f = g + h

where g is the number of steps taken so far, and h is an optimistic
estimation of the number of steps left, the heuristic.
"""

from queue import PriorityQueue
from field import field, start, target

def h(node):
    # Manhattan heuristic
    return abs(target[1] - node[1]) + abs(target[0] - node[0])

def find_neighbors(pos):
    found = []
    for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ind = (pos[0] + d[0], pos[1] + d[1])
        if field[ind[0]][ind[1]] != "#":
            found.append(ind)
    return found

q = PriorityQueue()
q.put((0 + h(start), start, []))  # use (priority, pos, history) tuples

visited = set()
while True:
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


## visualize
import matplotlib.pyplot as plt; plt.ion()
import numpy as np
board = np.array([[c == '#' for c in row] for row in field], dtype=int)
for his in history:
    board[his] = 2
board[start] = 3
board[target] = 3
plt.imshow(board)