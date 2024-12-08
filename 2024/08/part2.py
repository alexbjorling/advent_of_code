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

# check all pairs for each frequency, and loop to the board edge on either side
nodes = set()
for freq, positions in antennas.items():
    for i in range(len(positions)):
        for j in range(i):
            pos1 = np.array(positions[i])
            pos2 = np.array(positions[j])

            # find all antinodes on the pos2 side
            n = 0
            while True:
                p = pos2 + n * (pos2 - pos1)
                if p[0] < 0 or p[0] >= M or p[1] < 0 or p[1] >= N:
                    break
                nodes.add(tuple(p))
                n += 1

            # find all antinodes on the pos1 side
            n = 0
            while True:
                p = pos1 + n * (pos1 - pos2)
                if p[0] < 0 or p[0] >= M or p[1] < 0 or p[1] >= N:
                    break
                nodes.add(tuple(p))
                n += 1

assert len(nodes) == 884
