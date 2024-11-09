import numpy as np

with open("input.txt", "r") as fp:
    im = fp.readline().strip()
    im = np.array([int(s) for s in im])

sh = (6, 25)
layers = int(len(im) / (sh[0] * sh[1]))
im = im.reshape((layers,) + sh)

# layer with the smallest number of zeros
layer = np.argmin(np.sum(im == 0, axis=(1, 2)))

# find ones and twos
ones = np.sum(im[layer] == 1)
twos = np.sum(im[layer] == 2)
assert ones * twos == 1072
