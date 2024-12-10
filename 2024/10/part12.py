import numpy as np

# load the data
data = []
with open("input.txt", "r") as fp:
    for line in fp:
        data.append(list(map(int, line.strip())))
data = np.array(data)
starts = [tuple(r) for r in np.array(np.where(data == 0)).T]

# recursive function
def find9(pos):
    """
    Returns a list of all the nines reached, one for each path taken.
    """
    n = data[pos]
    if n == 9:
        return [pos,]

    nines = []
    M, N = data.shape
    for way in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_pos = (pos[0] + way[0], pos[1] + way[1])
        if new_pos[0] < 0 or new_pos[0] >= M or new_pos[1] < 0 or new_pos[1] >= N:
            continue
        if data[new_pos] == n + 1:
            nines += find9(new_pos)

    return nines

# sum up the calculation for each starting point
totA = 0
totB = 0
for start in starts:
    nines = find9(start)
    totA += len(set(nines))
    totB += len(nines)

assert totA == 820
assert totB == 1786