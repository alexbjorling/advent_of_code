import numpy as np

# load the data as an array
data = []
with open("input.txt", "r") as fp:
    for line in fp:
        data.append([ord(c) for c in line.strip()])
data = np.array(data)
M, N = data.shape

# go through the antennas and make a dict of {frequency: [positions...]}
antennas = {}
locations = np.where(data != ord("."))
for i, j in zip(locations[0], locations[1]):
    frequency = data[i, j]
    if frequency in antennas:
        antennas[frequency].append((i, j))
    else:
        antennas[frequency] = [(i, j)]

# check all pairs for each frequency, collect the antinodes that are within the board
nodes = set()
for freq, positions in antennas.items():
    for i in range(len(positions)):
        for j in range(i):
            pos1 = np.array(positions[i])
            pos2 = np.array(positions[j])
            n1 = 2 * pos2 - pos1
            n2 = 2 * pos1 - pos2
            if n1[0] >= 0 and n1[0] < M  and n1[1] >= 0 and n1[1] < N:
                nodes.add(tuple(n1))
            if n2[0] >= 0 and n2[0] < M  and n2[1] >= 0 and n2[1] < N:
                nodes.add(tuple(n2))

assert len(nodes) == 222
