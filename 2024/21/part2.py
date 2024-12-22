"""
Fast, cached, and recursive solution. runs in a few milliseconds.
"""

from functools import lru_cache

# load the data
with open("input.txt", "r") as fp:
    data = [l.strip() for l in fp.read().splitlines()]

# keypad definitions
keypad = {
    '7': (0, 0),
    '8': (0, 1),
    '9': (0, 2),
    '4': (1, 0),
    '5': (1, 1),
    '6': (1, 2),
    '1': (2, 0),
    '2': (2, 1),
    '3': (2, 2),
    '0': (3, 1),
    'A': (3, 2),
}
keypad_avoid = (3, 0)

robot = {
    '^': (0, 1),
    'A': (0, 2),
    '<': (1, 0),
    'v': (1, 1),
    '>': (1, 2),
}
robot_avoid = (0, 0)

# Helper to recursively find all combinations of sequences that will go
# from start_pos to end_pos, avoiding the specified blank square.
def options(end_pos, start_pos, avoid):
    if end_pos == start_pos:
        return ['']

    di = end_pos[0] - start_pos[0]
    dj = end_pos[1] - start_pos[1]
    vertical = 'v' if di > 0 else '^'
    horizontal = '>' if dj > 0 else '<'
    if di == 0:
        # moving just horizontally, no danger
        return [horizontal + x for x in options(end_pos, (start_pos[0], start_pos[1] + int(dj / abs(dj))), avoid)]
    elif dj == 0:
        # moving just vertically, no danger
        return [vertical + x for x in options(end_pos, (start_pos[0] + int(di / abs(di)), start_pos[1]), avoid)]
    else:
        # moving both, have to check for the gap
        di_sign = int(di / abs(di))
        dj_sign = int(dj / abs(dj))
        opts = []
        if (start_pos[0], start_pos[1] + dj_sign) != avoid:
            opts += [horizontal + x for x in options(end_pos, (start_pos[0], start_pos[1] + dj_sign), avoid)]
        if (start_pos[0] + di_sign, start_pos[1]) != avoid:
            opts += [vertical + x for x in options(end_pos, (start_pos[0] + di_sign, start_pos[1]), avoid)]
        return opts

# Return a list of the paths that will press the final code on the last keypad,
# the starting sequences for our robot chain.
def find_initial(code):
    pos = keypad['A']
    paths = ['']
    for c in code:
        new_paths = []
        for p in paths:
            for o in options(keypad[c], pos, keypad_avoid):
                new_paths.append(p + o + 'A')
        paths = new_paths
        pos = keypad[c]
    return paths

# Main recursive loop, which determines the cheapest way to produce
# a single keypress on a directional robot keypad, using N robots.
@lru_cache()
def shortest_single(char, last="A", N=25):
    # Are we done? If so, pressing the key takes one press.
    if N == 0:
        return 1

    # What are the options for producing our keypress using the next robot,
    # given that the next robot already stands at the last key? Find the
    # possible movement sequences to the wanted key, and add "A" to each.
    opts = options(robot[char], robot[last], robot_avoid)
    opts = [o + "A" for o in opts]

    # Loop over the options, summing up the individual keys for each, and
    # choose the option with the lowest total cost.
    opt_lengths = []
    for opt in opts:
        opt_length = 0
        last_ = "A"  # start again from A for each new robot
        for c_ in opt:
            opt_length += shortest_single(c_, last_, N-1)
            last_ = c_
        opt_lengths.append(opt_length)
    return min(opt_lengths)

tot = 0
for code in data:
    # Find the starting sequences that the robot chain should act on
    paths = find_initial(code)

    # Go through each starting path, sum up the lengths of the presses for each
    lengths = []
    for p in paths:
        last = "A"
        path_tot = 0
        for c in p:
            path_tot += shortest_single(c, last=last, N=25)
            last = c
        lengths.append(path_tot)
    tot += min(lengths) * int(code[:-1])

assert tot == 167538833832712