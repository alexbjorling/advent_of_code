import re
import numpy as np

# parse and get the starting nodes
network = {}
with open('input.txt', 'r') as fp:
    instructions = fp.readline().strip()
    fp.readline()
    for line in fp:
        node, left, right = re.match('(.{3}) = \((.{3}), (.{3})\)', line.strip()).groups()
        network[node] = {'L': left, 'R': right}
current = [k for k in network.keys() if k.endswith('A')]

# Noticed that the paths are periodic. So loop to find the periodicities
# of each trajectory.
periods = [[] for i in range(len(current))]
steps = 0
for ii in range(1000):
    for direction in instructions:
        # update the whole list of current positions
        steps += 1
        for i in range(len(current)):
            current[i] = network[current[i]][direction]
            if current[i].endswith('Z'):
                periods[i].append(steps)

# so we get this list of prime numbers
periodicities = [np.diff(p)[0] // len(instructions) for p in periods]

# what is the first number which is divisible by all these?
intersection = np.prod(periodicities).astype(int) * len(instructions)

intersection == 13740108158591