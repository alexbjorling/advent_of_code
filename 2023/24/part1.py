import re
import numpy as np


class Stone:
    def __init__(self, pos, vel):
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        # find the line equation for the trajectory
        assert self.vel[0] != 0  # line eqns don't work for vertical lines
        p2 = self.pos + self.vel
        self.k = (p2[1] - self.pos[1]) / (p2[0] - self.pos[0])  # slope
        self.m = self.pos[1] - self.k * self.pos[0]


stones = []
with open('input.txt', 'r') as fp:
    for line in fp:
        px, py, vx, vy = list(map(int, re.match('(-?\d+),\s*(-?\d+).*@\s*(-?\d+),\s*(-?\d+).*', line).groups()))
        stones.append(Stone(pos=(px, py), vel=(vx, vy)))

pmin = 200000000000000
pmax = 400000000000000

total = 0
for i in range(len(stones)):
    for j in range(i):
        s1, s2 = stones[i], stones[j]
        # stones parallel?
        if np.allclose(s1.k, s2.k):
            continue
        # where do they cross then?
        if np.allclose(s1.k, s2.k):
            print(s1.vel, s2.vel)
        x = (s2.m - s1.m) / (s1.k - s2.k)
        y = s1.k * x + s1.m
        # outside the test area?
        if x < pmin or x > pmax or y < pmin or y > pmax:
            continue
        # is this in the future of both stones?
        xy = np.array((x, y))
        t1 = ((xy - s1.pos) / s1.vel)[0]
        t2 = ((xy - s2.pos) / s2.vel)[0]
        if t1 > 0 and t2 > 0:
            total += 1

assert total == 25261
