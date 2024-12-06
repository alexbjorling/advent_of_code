import numpy as np
import sys
sys.setrecursionlimit(10000)

# load data
data = []
with open("input.txt", "r") as fp:
    for line in fp.read().strip().split('\n'):
        data.append([ord(c) for c in line.strip()])
data = np.array(data)

# some definitions
guard = ord("^")
free = ord(".")
block = ord("#")

# find the guard position
pos = np.where(data == guard)
pos = (pos[0][0], pos[1][0])

def step(state, extra=(-1, -1)):
    # step the state (i, j, vi, vj) forward, by moving or turning
    m, n = data.shape
    pos = state[:2]
    vel = state[2:]
    facing = pos[0] + vel[0], pos[1] + vel[1]
    if (data[facing] == block) or (facing == extra):
        right = np.array(((0, 1), (-1, 0)))
        state = pos + tuple(np.dot(right, vel))           # new state, just turned
    else:
        state = (pos[0] + vel[0], pos[1] + vel[1]) + vel  # new state, just moved
    return state

def count_squares(state, visited=set()):
    pos = state[:2]
    m, n = data.shape
    visited.add(state)
    if pos[0] == 0 or pos[1] == 0 or pos[0] == m - 1 or pos[1] == n - 1:
        squares = set([t[:2] for t in visited])
        return len(squares)
    else:
        new_state = step(state)
        return count_squares(new_state, visited)

assert 5162 == count_squares(pos + (-1, 0))
