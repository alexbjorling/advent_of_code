"""
Very bad and slow solution, took a long time to realize it was a search problem,
and then didn't realize you can evaluate a single character all the way down,
so instead made all explicit combinations, which takes forever.
"""

# keypads
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

# load the data
with open("input.txt", "r") as fp:
    data = [l.strip() for l in fp.read().splitlines()]


# recursively find all combinations of sequences that will go from pos to button
# on the specified keypad, avoiding the blank
def options(button, pad, pos):
    target = pad[button]
    if target == pos:
        return ['']

    di = target[0] - pos[0]
    dj = target[1] - pos[1]
    vertical = 'v' if di > 0 else '^'
    horizontal = '>' if dj > 0 else '<'
    if di == 0:
        # moving just horizontally, no danger
        return [horizontal + x for x in options(button, pad, (pos[0], pos[1] + int(dj / abs(dj))))]
    elif dj == 0:
        # moving just vertically, no danger
        return [vertical + x for x in options(button, pad, (pos[0] + int(di / abs(di)), pos[1]))]
    else:
        # moving both, have to check for the gap
        di_sign = int(di / abs(di))
        dj_sign = int(dj / abs(dj))
        opts = []
        avoid = keypad_avoid if pad == keypad else robot_avoid
        if (pos[0], pos[1] + dj_sign) != avoid:
            opts += [horizontal + x for x in options(button, pad, (pos[0], pos[1] + dj_sign))]
        if (pos[0] + di_sign, pos[1]) != avoid:
            opts += [vertical + x for x in options(button, pad, (pos[0] + di_sign, pos[1]))]
        return opts

def press_seq(pad, seq):
    pos = 'A'
    paths = ['']
    for c in seq:
        new_paths = []
        for p in paths:
            for o in options(c, pad, pad[pos]):
                new_paths.append(p + o + 'A')
        paths = new_paths
        pos = c
    return paths

tot = 0
for code in data:
    lens = []
    for seq in press_seq(keypad, code):
        for seq2 in press_seq(robot, seq):
            for seq3 in press_seq(robot, seq2):
                lens.append(len(seq3))
    print(min(lens))
    tot += min(lens) * int(code[:-1])

assert tot == 136780