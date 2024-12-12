import numpy as np
import sys

sys.setrecursionlimit(10000)

# load the data
data = []
with open("input.txt", "r") as fp:
    for line in fp:
        data.append([ord(c) for c in line.strip()])
data = np.array(data)

def fill(pos, patch=None):
    """
    Find all positions connected to pos by pixels of the same value, return them as a set.
    """
    if patch is None:
        patch = set()

    patch.add(pos)

    M, N = data.shape
    for way in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        new_pos = (pos[0] + way[0], pos[1] + way[1])
        if min(new_pos) < 0 or new_pos[0] >= M or new_pos[1] >= N:
            continue
        if (new_pos not in patch) and (data[new_pos] == data[pos]):
            patch = patch.union(fill(new_pos, patch))

    return patch

def boundary(region):
    """
    Takes a set of region positions and returns its boundary, as ((inside_pos), (outside direction))
    """
    tot = 0
    boundary = set()
    for pos in region:
        for way in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new_pos = (pos[0] + way[0], pos[1] + way[1])
            if not new_pos in region:
                direction = (new_pos[0]-pos[0], new_pos[1]-pos[1])
                boundary.add((pos, direction))
    return boundary

def sides(bound):
    """
    Takes a set of boundaries on the above format by sorting all the
    boundary pieces and only counting those not connected to any
    already accounted for.
    """
    bound = sorted(bound)
    tot = 0
    for i in range(len(bound)):
        count = 1
        for j in range(i):
            # is this boundary piece connected to a piece we've already counted?
            same_direction = (bound[i][1] == bound[j][1])
            di = bound[i][0][0] - bound[j][0][0]
            dj = bound[i][0][1] - bound[j][0][1]
            neighbors = (abs(di) + abs(dj) == 1)
            if same_direction and neighbors == 1:
                count = 0
                break
        tot += count
    return tot

covered = np.zeros_like(data)
totA = 0
totB = 0
while covered.sum() < np.prod(data.shape):
    # get any position not covered yet, and find its region
    pos = tuple(np.array(np.where(covered == 0)).T[0])
    new_patch = fill(pos)

    # sum up the respective costs for the patch
    totA += len(new_patch) * len(boundary(new_patch))
    totB += len(new_patch) * sides(boundary(new_patch))

    # mark all these squares as covered
    for p in new_patch:
        covered[p] = 1

assert totA == 1370258
assert totB == 805814
