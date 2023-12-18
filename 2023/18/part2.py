import numpy as np
import re

# make an array of vertices
dir_map = {'0': np.array((0, 1)), '2': np.array((0, -1)), '3': np.array((-1, 0)), '1': np.array((1, 0))}
steps = []
with open('input.txt', 'r') as fp:
    for line in fp:
        hex = re.search('.*\#([a-f,0-9]+)', line).groups()[0]
        length = eval('0x' + hex[:-1])
        direction = dir_map[hex[-1]]
        steps.append(direction * length)
vertices = np.cumsum(steps, axis=0)
assert (vertices[-1] == np.array((0,0))).all()

# use some magical linear algebra (https://en.wikipedia.org/wiki/Shoelace_formula)
total = 0
N = vertices.shape[0]
for i in range(N-1):
    a = [[vertices[i][0], vertices[i+1][0]], [vertices[i][1], vertices[i+1][1]]]
    total += np.linalg.det(a)

area = np.abs(total) / 2
edge = np.sum(np.abs(steps))

assert int(area + edge//2) + 1 == 44644464596918  ## the +1 is from the starting block (I think)
