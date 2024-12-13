"""
Solve the 2x2 linear equation for A- and B-key presses Na and Nb.

    Na * ax + Nb * bx = px
    Nb * ay + Nb * by = py

When there is a solution with integer Na and Nb, we can get the prize.
There are no underdefined systems of equations here, if there were we
would have to find the minimum.
"""

import re
import numpy as np

class Machine:
    def __init__(self, A, B, prize):
        self.M = [[A[0], B[0]], [A[1], B[1]]]
        self.prize = prize

machines = []
with open("input.txt", "r") as fp:
    data = fp.read().split("\n\n")
    for d in data:
        numbers = list(map(int, re.findall(("\d+"), d)))
        machines.append(Machine(numbers[:2], numbers[2:4], numbers[-2:]))

cost = 0
for i, m in enumerate(machines):
    np.linalg.inv(m.M)  # throws if there are multiple solutions
    soln = np.linalg.solve(m.M, m.prize)
    if np.all(np.isclose(soln, np.round(soln), rtol=0, atol=.001)):
        cost += int(round(soln[0] * 3 + soln[1]))

assert cost == 39996
