"""
Solve part 1 in a more general and efficient way, using numpy a lot.
"""

import numpy as np

# load the data as an array of ascii values
field = []
data = []
with open("input.txt", "r") as fp:
    for line in fp:
        field.append([ord(c) for c in line.strip()])
field = np.array(field)
wall = ord("#")

# embed the field in some thick walls to make things easier
N = field.shape[0]
new_field = np.ones((N + 100,) * 2) * wall
new_field[50:50+N, 50:50+N] = field
field = new_field

# find start and target
start = tuple(np.array(np.where(field == ord("S"))).T[0])
target = tuple(np.array(np.where(field == ord("E"))).T[0])

# set the walls to -1 to avoid confusion later
wall = ord("#")
field[np.where(field == wall)] = -1
wall = -1

# first, find the standard track and label the squares with the step number
pos = start
track = []
while pos != target:
    field[pos] = len(track)
    ways = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for way in ways:
        ind = (pos[0] + way[0], pos[1] + way[1])
        if field[ind] != wall and (ind not in track):
            track.append(pos)
            pos = ind
            break
track.append(pos)
field[pos] = len(track) - 1

# prepare some arrays for searching
N = 20
hood_inds = np.indices((2 * N + 1,) * 2) - N
hood_path = np.sum(np.abs(hood_inds), axis=0)
hood_mask = hood_path <= N

# now go through the track, searching for shortcuts from each square
tot = 0

for pos in track:
    local = field[hood_inds[0] + pos[0], hood_inds[1] + pos[1]]
    gains = ((local != wall) & hood_mask) * (local - field[pos] - hood_path)
    tot += np.sum(gains >= 100)

assert tot == 988931