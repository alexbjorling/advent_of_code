"""
Same method as in part 1, but now we can't ignore pahts via nodes already
visited. Instead, we have to see if the same state has been visited at a
lower cost.

So, visited is a dict {state: cost}, with state a 4-tuple like before.
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
q.put((0, start, set()))  # use (cost so far, pos, history) tuples

best_cost = 0
visited = dict()
seen = 0

while q.qsize():
    # pick a node to move forward!
    f, node, history = q.get(timeout=0)  # will fail if empty

    # progress printing
    if len(history) > seen:
        seen = len(history)
        print(seen)

    # see if we've reached the target, and if so at what cost
    if node[:2] == target:
        if best_cost == 0:  # first time
            histories = set(history)
            best_cost = f
            print(f"Got there at cost {f}, {len(history) + 1} long")
        elif f == best_cost:
            histories = histories.union(history)
            print(f"  ...another cost {f}, {len(history) + 1} long")
        else:
            print("Found a more expensive path, we're done")
            break

    # find the neighbors n_ with additional cost c_
    neighbors = find_neighbors(node)
    for n_, c_ in neighbors.items():
        if n_ in visited.keys() and (f + c_) > visited[n_]:
            continue

        q.put((f + c_, n_, history.union(set((node[:2],)))))
        visited[n_] = f + c_

assert len(histories) + 1 == 502