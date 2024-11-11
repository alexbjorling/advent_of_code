from Intcode import Intcode

with open("input.txt", "r") as fp:
    prog = list(map(int, fp.readline().split(",")))
comp = Intcode(prog)

painted = {}
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

assert len(painted) == 2478