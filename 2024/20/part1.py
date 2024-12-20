import numpy as np
from collections import defaultdict

# load the data as an array of ascii values
field = []
data = []
with open("input.txt", "r") as fp:
    for line in fp:
        field.append([ord(c) for c in line.strip()])
field = np.array(field)
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

# now go through the track, searching for shortcuts from each square (there
# are no diagonal shortcuts, but there could have been...)
tot = defaultdict(int)
for pos in track:
    ways = ((2, 0), (-2, 0), (0, 2), (0, -2))
    for way in ways:
        ind = (pos[0] + way[0], pos[1] + way[1])
        if min(ind) >= 0 and max(ind) < field.shape[0] and field[ind] != wall:
            gain = field[pos] - field[ind] - 2
            if gain >= 100:
                tot[gain] += 1

assert sum(tot.values()) == 1429
