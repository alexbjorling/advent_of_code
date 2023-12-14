import numpy as np

# read
with open('input.txt', 'r') as fp:
    patterns = fp.read().split('\n\n')
    patterns = [p.split() for p in patterns]

# ascii codes for # and .
dot, cross = np.frombuffer('.#'.encode(), dtype=np.uint8)

# helpers for finding planes
def find_vertical_mirror(d, excl=-1):
    for i in range(1, d.shape[1]):
        if i == excl:
            continue
        width = min(i, d.shape[1] - i)
        if (d[:, i-width:i] == d[:, i:i+width][:, ::-1]).all():
            return i
            
def find_horizontal_mirror(d, excl=-1):
    for i in range(1, d.shape[0]):
        if i == excl:
            continue
        width = min(i, d.shape[0] - i)
        if (d[i-width:i, :] == d[i:i+width, :][::-1, :]).all():
            return i

total = 0
for pattern in patterns:

    # wrap a numpy array around the string so we can operate on rows and columns
    shape = len(pattern), len(pattern[0])
    data = np.copy(np.frombuffer(''.join(pattern).encode(), dtype=np.uint8).reshape(shape))
    data[np.where(data == cross)] = 0
    data[np.where(data == dot)] = 1

    # first find the original mirror line so we can exclude it
    v0 = find_vertical_mirror(data)
    h0 = find_horizontal_mirror(data)

    # go over all the positions, flip their values and look for reflections
    for pos in range(np.prod(shape)):

        inds = np.unravel_index(pos, shape)
        data_ = np.copy(data)
        data_[inds] = 1 - data_[inds]

        r = find_vertical_mirror(data_, v0)
        if r:
            total += r

        # look for horizontal mirror lines
        r = find_horizontal_mirror(data_, h0)
        if r:
            total += r * 100

assert total // 2 == 34224  # double counting mirrored smudges
