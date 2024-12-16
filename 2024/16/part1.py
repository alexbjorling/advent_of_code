"""
Do a breadth-first search in priority order of the cost so far. Equivalent
to A* with heuristic h = 0.

This is a good idea, because the heuristic is not much use in a situation
where the cost varies a lot depending on whether you turn or not, and
where there are labyrinth-like walls everywhere.

The state is a 4-tuple with positions and directions.
"""

import numpy as np
from queue import PriorityQueue

# load the data as an array of ascii values
field = []
with open("input.txt", "r") as fp:
    for line in fp:
        field.append([ord(c) for c in line.strip()])
field = np.array(field)
wall = ord("#")
start = tuple(np.array(np.where(field == ord("S"))).T[0]) + (0, 1)
target = tuple(np.array(np.where(field == ord("E"))).T[0])

# helper to identify possible neighbors and the additional cost of getting there, {n_: c_}
def find_neighbors(state):
    found = {}
    pos = state[:2]
    vel = state[2:]
    # continue straight, if poss
    straight = (pos[0] + vel[0], pos[1] + vel[1])
    if field[straight] != wall:
        found[(straight + vel)] = 1
    # turn, always
    vright = tuple(np.dot([[0, 1],[-1, 0]], vel))
    vleft = tuple(np.dot([[0, -1],[1, 0]], vel))
    found[pos + vright] = 1000
    found[pos + vleft] = 1000
    return found

q = PriorityQueue()
q.put((0, start, []))  # use (cost so far, pos, history) tuples

visited = set()
while q.qsize():
    # pick a node to move forward!
    f, node, history = q.get(timeout=0)  # will fail if empty

    # see if we're finished
    if node[:2] == target:
        print(f"Got there at cost {f}")
        break

    # find the neighbors n_ with additional cost c_
    neighbors = find_neighbors(node)
    for n_, c_ in neighbors.items():
        if n_ in visited:
            continue

        q.put((f + c_, n_, history+[node,]))
        visited.add(n_)

assert f == 94444