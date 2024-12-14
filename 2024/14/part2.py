"""
Look for a situation where there's only one robot per position, which
only happens on the easter egg.
"""

import re

# load the data naively
robots = []
with open("input.txt", "r") as fp:
    for line in fp:
        numbers = list(map(int, re.findall("(\-?\d+)", line)))
        robots.append((numbers[:2], numbers[2:]))

shape = [101, 103]

# this time we have to loop
n = 0
while True:
    n += 1

    # step all the robots forward
    for i, r in enumerate(robots):
        pos, vel = r
        pos = (
            (pos[0] + vel[0]) % shape[0],
            (pos[1] + vel[1]) % shape[1],
        )
        robots[i] = (pos, vel)

    # compare the set of unique positions with the number of robots
    unique = {p for p, v in robots}
    if len(unique) == len(robots):
        break

assert n == 6475


# show the tree
import matplotlib.pyplot as plt; plt.ion()
import numpy as np
im = np.zeros(shape[::-1], dtype=int)
for r in robots:
    pos, vel = r
    im[pos[::-1]] += 1
plt.imshow(im)
