"""
A* is wrapped in a function, we do a bisection search to find the fatal last byte.
"""

import numpy as np

from queue import PriorityQueue
inds = []
with open("input.txt", "r") as fp:
    for line in fp:
        j, i = map(int, line.strip().split(","))
        inds.append((i, j))

start = (0, 0)
target = (70, 70)
latest = (0, 0)

def attempt(N):
    """
    Attempt to solve the labyrinth after dropping N blocks. Returns
    True (solved it) or False (didn't solve it).
    """
    global latest

    # fill in the playing field
    field = np.zeros((71, 71), dtype=int)
    for ind in inds[:N]:
        field[ind[0], ind[1]] = 1

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
    q.put((0 + h(start), start))  # use (priority, pos) tuples

    visited = set()
    while q.qsize():
        # pick a node to move forward!
        f, node = q.get(timeout=0)  # will fail if empty

        # see if we're finished
        if node == target:
            return True

        # find the neighbors and update their f values
        neighbors = find_neighbors(node)
        g = f - h(node)  # path taken so far
        for n_ in neighbors:
            if n_ in visited:
                continue

            f = g + 1 + h(n_)
            q.put((f, n_))
            visited.add(n_)

    # if we get here the queue is empty and we can't solve the maze
    latest = inds[N - 1][::-1]
    return False

n1 = 0
n3 = len(inds) - 1
n2 = (n3 - n1) // 2

while n3 - n1 > 2:
    if attempt(n2):
        # middle point is solvable, look between n2 and n3
        n1 = n2
    else:
        # middle point is not solvable, look between n1 and n2
        n3 = n2
    n2 = n1 + (n3 - n1) // 2

assert latest == (45, 16)