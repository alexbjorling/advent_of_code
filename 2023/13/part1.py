import numpy as np

# read
with open('ex.txt', 'r') as fp:
    patterns = fp.read().split('\n\n')
    patterns = [p.split() for p in patterns]

total = 0
for pattern in patterns:

    # wrap a numpy array around the string so we can operate on rows and columns
    shape = len(pattern), len(pattern[0])
    data = np.frombuffer(''.join(pattern).encode(), dtype=np.uint8).reshape(shape)

    # look for vertical mirror lines
    for i in range(1, shape[1]):
        width = min(i, shape[1] - i)
        if (data[:, i-width:i] == data[:, i:i+width][:, ::-1]).all():
            total += i

    # look for horizontal mirror lines
    for i in range(1, shape[0]):
        width = min(i, shape[0] - i)
        if (data[i-width:i, :] == data[i:i+width, :][::-1, :]).all():
            total += i * 100

assert total == 34889
