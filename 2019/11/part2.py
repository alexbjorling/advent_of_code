from Intcode import Intcode

with open("input.txt", "r") as fp:
    prog = list(map(int, fp.readline().split(",")))
comp = Intcode(prog)

# do the calculation
painted = {}
painted[(0, 0)] = 1   # new for part 2
coord = (0, 0)
direction = (-1, 0)
while not comp.halted:
    current = painted.get(coord, 0)
    painted[coord] = comp.run([current,], return_on_output=True)
    turn = comp.run(return_on_output=True)
    if turn:    # right 90 degrees
        direction = (direction[1], -direction[0])
    else:       # left 90 degrees
        direction = (-direction[1], direction[0])
    coord = (coord[0] + direction[0], coord[1] + direction[1])

# render the message
import numpy as np
a = np.zeros((50, 100), dtype=int)
for k, v in painted.items():
    a[k[0], k[1]] = "1" if v else 0
txt = ''
for i in range(a.shape[0]):
    txt += ''.join(map(str, a[i, :])).replace('0', ' ').replace('1', 'X') + '\n'
print(txt) # HCZRUGAZ
