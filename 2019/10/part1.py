import numpy as np

# for ex.txt the max is 33
with open("input.txt", "r") as fp:
    data = [l.strip().replace("#", "1").replace(".", "0") for l in fp]

# make a nice array and a list of coordingates
table = np.array([[int(c) for c in row] for row in data])
ast = list(zip(*np.where(table)))

# make a table of pairwise line of sight
los = np.zeros((len(ast),) * 2, dtype = int)
for n1 in range(len(ast)):
    for n2 in range(n1):
        visible = 1
        for n3 in range(len(ast)):
            if n3 in (n1, n2): continue
            i1, j1 = ast[n1]
            i2, j2 = ast[n2]
            i3, j3 = ast[n3]

            # only consider blocking stars in the rectangle of n1 and n2
            if (
                (i3 > i1 and i3 > i2)
                or (i3 < i1 and i3 < i2)
                or (j3 > j1 and j3 > j2)
                or (j3 < j1 and j3 < j2)
            ): continue

            # define two vectors and see if they are colinear
            v1 = (i3 - i1, j3 - j1)
            v2 = (i2 - i3, j2 - j3)
            dot_prod_2 = (v1[0] * v2[0] + v1[1] * v2[1])**2
            norm_prod_2 = (v1[0]**2 + v1[1]**2) * (v2[0]**2 + v2[1]**2)
            if dot_prod_2 == norm_prod_2:
                visible = 0
                break

        los[n1, n2] = visible
        los[n2, n1] = visible

# the maximum is easy to find now
assert los.sum(axis=1).max() == 347

print("best position at", ast[np.argmax(los.sum(axis=1))])