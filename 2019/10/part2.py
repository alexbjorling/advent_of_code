import numpy as np

# for ex.txt the max is 33
with open("input.txt", "r") as fp:
    data = [l.strip().replace("#", "1").replace(".", "0") for l in fp]

# make a nice array and a list of coordingates
table = np.array([[int(c) for c in row] for row in data])
ast = list(zip(*np.where(table)))

center = 36, 26  # ij

# convert to radial coordinates
phi, r2 = [], []
table_ = table.copy()
#table_[:] = -1
for a in ast:
    di = a[0] - center[0]
    dj = a[1] - center[1]
    r2.append(di**2 + dj**2)
    phi.append(np.arctan2(-dj-1e-15, di) + np.pi)
    table_[a[0], a[1]] = phi[-1]
phi = np.array(phi)
r2 = np.array(r2)
table_[center[0], center[1]] = 9

# go through and shift shadowed asteroids by 2pi
for i in range(len(phi)):
    twins = np.where(np.isclose(phi, phi[i]))[0]
    r_order = np.argsort(r2[twins])
    for j in range(len(twins)):
        phi[twins[r_order[j]]] += j * 2 * np.pi

# now everything is sorted
order = np.argsort(phi)
assert (ast[order[199]][1] * 100 + ast[order[199]][0]) == 829
