from Intcode import Intcode
import numpy as np

with open("input.txt", "r") as fp:
    prog = list(map(int, fp.readline().strip().split(",")))

comp = Intcode(prog)
output = []
while not comp.halted:
    output.append(
        [comp.run(return_on_output=True) for i in range(3)]
    )

n = np.sum(np.array(output)[:, 2] == 2)
assert n == 412