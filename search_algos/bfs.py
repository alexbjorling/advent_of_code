"""
Example BFS implementation,

"""

from field import field, start, target

def find_neighbors(pos):
    found = []
    for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ind = (pos[0] + d[0], pos[1] + d[1])
        if field[ind[0]][ind[1]] != "#":
            found.append(ind)
    return found

q = []
q.append((start, []))  # use (pos, history)

visited = set()
while q:
    # pick a node to move forward!
    node, history = q.pop(0)

    # see if we're finished
    if node == target:
        f = len(history) # steps taken, not positions tested
        print(f"Got there in {f} steps")
        break

    # find the neighbors and update their f values
    neighbors = find_neighbors(node)
    for n_ in neighbors:
        if n_ in visited:
            continue
        q.append((n_, history+[node,]))
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