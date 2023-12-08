import re

network = {}
with open('input.txt', 'r') as fp:
    instructions = fp.readline().strip()
    fp.readline()
    for line in fp:
        node, left, right = re.match('([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)', line.strip()).groups()
        network[node] = {'L': left, 'R': right}

done = False
current = 'AAA'
steps = 0
while not done:
    for direction in instructions:
        current = network[current][direction]
        steps += 1
        if current == 'ZZZ':
            done = True
            break

assert steps == 11309
