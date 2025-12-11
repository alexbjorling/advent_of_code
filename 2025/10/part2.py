import numpy as np
import re
from queue import PriorityQueue

# parse an input row to a system of equations A x = b, return (A, b)
def parse(row):
    # read the numbers of the buttons to press
    buttons = re.findall("\\((.*?)\\)", row)
    buttons = [re.findall("([0-9]+)", b) for b in buttons]
    buttons = [list(map(int, b)) for b in buttons]

    # read the sums, ie the joltage levels
    sums = re.findall("\\{(.*?)\\}", row)[0]
    sums = sums.split(",")
    sums = np.array(list(map(int, sums)), dtype=int)

    # convert the button presses to basis vectors
    bases = np.empty((sums.size, len(buttons)), dtype=int)
    for j, b in enumerate(buttons):
        v = np.zeros(len(sums), dtype=int)
        for p in b:
            v[p] += 1
        bases[:, j] = v

    return bases, sums

def find_neighbors(x):
    ret = []
    for i in range(x.size):
        x_ = np.copy(x)
        x_[i] += 1
        ret.append(x_)
        if x[i] > 0:
            x_ = np.copy(x)
            x_[i] += 1
            ret.append(x_)
    return ret

def h(A, x, b):
    return np.linalg.norm(np.dot(A, x) - b)

with open("ex.txt", "r") as fp:
    tot = 0
    for row in fp:
        A, b = parse(row)

        q = PriorityQueue()
        start = (0,) * A.shape[1]
        q.put((h(A, start, b), 0, start))  # use (priority, steps taken, vec) tuples

        visited = set()
        while True:
            # pick a node vector to move forward!
            f, g, x = q.get(timeout=0)  # will fail if empty
            x = np.array(x) # can't store ndarrays in a (sorted) priority queue
            #print(np.dot(A, x), b)

            # see if we're finished
            if np.all(np.dot(A, x) == b):
                print(f"Got there in {f} steps")
                tot += f
                break

            # find the neighbors and update their f values
            neighbors = find_neighbors(x)
            for x_ in neighbors:
                tuple_x_ = tuple(x_)
                if tuple_x_ in visited:
                    continue
                f = g + 1 + h(A, x_, b)
                q.put((f, g + 1, tuple_x_))
                visited.add(tuple_x_)

    print(f"total = {tot}")
