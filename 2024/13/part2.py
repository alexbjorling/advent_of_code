"""
Same solution as part 1.
"""

import re
import numpy as np

class Machine:
    def __init__(self, A, B, prize):
        self.M = [[A[0], B[0]], [A[1], B[1]]]
        self.prize = [p + 10000000000000 for p in prize]

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

assert cost == 73267584326867
