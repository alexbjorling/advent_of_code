from Intcode import Intcode
import numpy as np
import matplotlib.pyplot as plt; plt.ion()


## Set up the computer
with open("input.txt", "r") as fp:
    prog = list(map(int, fp.readline().strip().split(",")))

comp = Intcode(prog)
dir_map = {
    1: (-1, 0),
    2: (1, 0),
    3: (0, -1),
    4: (0, 1),
}
inv_dir_map = {v:k for k,v in dir_map.items()}
opposites = {1: 2, 2: 1, 3: 4, 4: 3}


## Now find the target by stupidest random walk
walls = []
blanks = []
atlas = {}
pos = np.array((0, 0))

def render(atlas):
    grid = np.array(list(atlas.keys()))
    N = np.max(np.abs(grid))
    field = np.ones((2 * N, 2 * N), dtype=int) * -1
    walls = np.array([k for k, v in atlas.items() if v == 0])
    blanks = np.array([k for k, v in atlas.items() if v == 1])
    field[walls[:, 0] + N, walls[:, 1] + N] = 0
    field[blanks[:, 0] + N, blanks[:, 1] + N] = 1
    return field

n = 0
if True:
    done = False
    while not done:
        n += 1

        # figure out what's nearby and what our options are
        useful_moves = []
        possible_moves = []
        for move in range(1, 5):
            test_pos = tuple(pos + np.array(dir_map[move]))
            moved = True
            if test_pos in atlas:
                ret = atlas[test_pos]
                moved = False
            else:
                ret = comp.run(move)
            if ret == 0:
                # note there's a wall, we haven't moved
                atlas[test_pos] = 0
            elif ret == 1:
                # move back but note there's a blank there
                if moved:
                    comp.run(opposites[move])
                possible_moves.append(move)
                unknown = test_pos not in atlas.keys()
                if unknown:
                    useful_moves.append(move)
                atlas[test_pos] = 1
            elif ret == 2:
                # we've found it
                target = test_pos
                print(f"Target is at {test_pos}")
                done = True

        # choose a move that explores new terrain if possible
        if len(useful_moves):
            move = useful_moves[0]
        else:
            move = possible_moves[np.random.randint(len(possible_moves))]
        comp.run(move)
        pos = tuple(pos + np.array(dir_map[move]))

        if n % 1000 == 0:
            print(n)

assert target == (14, 14)
plt.imshow(render(atlas))
