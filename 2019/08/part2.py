import numpy as np

# load and shape data
with open("input.txt", "r") as fp:
    im = fp.readline().strip()
    im = np.array([int(s) for s in im])
sh = (6, 25)
layers = int(len(im) / (sh[0] * sh[1]))
im = im.reshape((layers,) + sh)

# find the layer determining the color for each pixel
color_layer = np.argmax((im < 2), axis=0)

# pick that layer for each pixel - faster with numpy somehow
msg = np.zeros(sh, dtype=int)
for i in range(sh[0]):
    for j in range(sh[1]):
        msg[i, j] = im[color_layer[i, j], i, j]

# render the message
txt = ''
for i in range(sh[0]):
    txt += ''.join(map(str, msg[i, :])).replace('0', ' ') + '\n'

print(txt)