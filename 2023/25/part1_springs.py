### Trying my own implementation of some naive spring+repulsion model

import numpy as np
import matplotlib.pyplot as plt
plt.ion()


# read the data and parse as list of nodes and dict of connections
conn = {}
nodelist = []
with open('input.txt', 'r') as fp:
    for line in fp:
        nodes_ = line.replace(':', '').split()
        nodelist += nodes_
        conn[nodes_[0]] = nodes_[1:]
nodelist = list(set(nodelist))
N = len(nodelist)


# let's work with two big x and y arrays for now
x = np.random.rand(N)
y = np.random.rand(N)
xy = np.stack((x, y), axis=1)
F_y = np.zeros_like(xy)


def plot(x, y, conn, nodelist, ax=None, labels=True, title=''):
    if ax:
        ax.clear()
    else:
        fig = plt.figure()
        ax = plt.gca()
    # nodes
    ax.set_title(title)
    ax.plot(x, y, 'o')
    # labels
    if labels:
        for i, lbl in enumerate(nodelist):
            ax.text(x[i], y[i], lbl)
    # connections
    for src in conn.keys():
        for dst in conn[src]:
            i = nodelist.index(src)
            j = nodelist.index(dst)
            ax.plot([x[i], x[j]], [y[i], y[j]], 'k', lw=.1)


# OK how do we set up these forces? Since we need all ij distances for the
# repulsion we might as well keep a big matrix of distances.

# encode the springs as off-diagonal matrix elements
springs = np.zeros((N, N), dtype=np.uint8)
for n1 in conn.keys():
    for n2 in conn[n1]:
        i1 = nodelist.index(n1)
        i2 = nodelist.index(n2)
        springs[i1, i2] = 1
        springs[i2, i1] = 1

fig, ax = plt.subplots()
for i in range(45):
    # get the pairwise distance by broadcasting shapes
    # these are now dx[i, j] = x[j] - x[i], so (dx[i, j], dy[i, j]) is the vector
    # from node i to node j.
    x, y = xy[:, 0], xy[:, 1]
    dx = x - x.reshape((-1, 1))
    dy = y - y.reshape((-1, 1))

    # Each node i therefore feels a spring force k * dx[i, j] from each of its
    # neighbors j, or in total sum_j(springs * dx) * k for the x part.
    k = 1
    F_k = k * np.array((np.sum(springs * dx, axis=1), np.sum(springs * dy, axis=1))).T

    # The repulsive force goes in the other direction, from j to our node i.
    q = 5e-4
    F_q = q * np.array((-np.sum(dx, axis=1), -np.sum(dy, axis=1))).T

    # Also add a force towards the x-axis, so they separate horizontally
    F_y[:, 1] = -2 * y

    # Update the positions
    xy[:] = xy + .1 * (F_k + F_q + F_y)

    print(i)

plot(x, y, conn, nodelist, ax=ax, labels=False, title=str(i))

# The groups separate along x
assert sum(x > .5) * sum(x < .5) == 543564
