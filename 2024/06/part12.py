import numpy as np
import time

# load data
data = []
with open("ex.txt", "r") as fp:
    for line in fp.read().strip().split('\n'):
        data.append([ord(c) for c in line.strip()])
data = np.array(data)
data0 = data.copy()

# some definitions
guard = ord("^")
free = ord(".")
block = ord("#")

def check_path(data, pos, dirc):
    """
    returns: (
        - the number of squares covered before the guard leaves the area, None means it never does,
        - an array of squares covered
    )
    """
    past_states = set()
    visited = np.zeros_like(data)
    while True:
        visited[tuple(pos)] = 1
        state = tuple(pos) + tuple(dirc)
        if state in past_states:
            return None, visited  # infinite
        past_states.add(state)
        # walk around
        facing = pos + dirc
        if facing[0] > -1 and facing[0] < len(data) and facing[1] > -1 and facing[1] < len(data[0]):
            if data[tuple(facing)] == block:
                dirc = np.dot(right, dirc)
            pos = pos + dirc
        else:
            return visited.sum(), visited

# find the guard position
pos = np.where(data == guard)
pos = np.array((pos[0][0], pos[1][0]))

# direction and rotation matrix
dirc = np.array((-1, 0))
right = np.array(((0, 1), (-1, 0)))

# copies for later
pos0 = pos.copy()
dirc0 = dirc.copy()

n, visited = check_path(data, pos, dirc)
print(n)
assert n == 5162

visited[tuple(pos0)] = 0
free_sites = np.array(np.where(visited)).T  # array
free_sites = [tuple(row) for row in free_sites]
infinite = 0
i = 0
for free_site in free_sites:
    i += 1
    data = data0.copy()
    if visited[free_site] == 0:
        print(i, free_site)
        raise ValueError
    data[free_site] = block
    dirc = dirc0.copy()
    pos = pos0.copy()
    t0 = time.time()
    n, _ = check_path(data, pos, dirc)
    if n is None:
        infinite += 1
    if i % 100 == 0:
        print(f"{i} / {len(free_sites)}, {(time.time() - t0):.3f} s/board")
print(infinite)