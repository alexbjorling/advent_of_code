from Intcode import Intcode
import numpy as np
import time

with open("input.txt", "r") as fp:
    prog = list(map(int, fp.readline().strip().split(",")))

prog[0] = 2  # hacks the program

comp = Intcode(prog)

def render_screen(a):
    block_map = {
        0: " ",
        1: "/",
        2: "X",
        3: "^",
        4: "O",
    }
    # renders the integer array of tile id:s into a game display
    txt = ''
    for row in a:
        for char in row:
            txt += (block_map[char])
        txt += "\n"
    return txt

screen = np.zeros((30,50), dtype=int)
ball = 0
paddle = 0
score = 0
while not comp.halted:
    x = comp.run()
    y = comp.run()
    val = comp.run()

    # need an input?
    if None in (x, y, val):
        inval = np.sign(ball - paddle)
        time.sleep(.01)
        comp.inputs.append(inval)
        continue

    # score or screen update?
    if x == -1 and y == 0:
        score = val
    else:
        if val == 3:
            paddle = x
        elif val == 4:
            ball = x
        screen[y, x] = val
        print(render_screen(screen))
        print("Score:", score)

assert score == 20940
