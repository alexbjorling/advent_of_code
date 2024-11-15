"""
Get astar running...
"""

import numpy as np
import matplotlib.pyplot as plt; plt.ion()

field = [
    '#############################',
    '#   S #            ##       #',
    '#     #            ##       #',
    '#     #            ##       #',
    '#     #            ##       #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ## X #',
    '#  #######    ##   ##  ##   #',
    '#             ##       ##   #',
    '#############################',
]

def find_char(field, char):
    start_row = ([char in row for row in field]).index(True)
    start_column = field[start_row].index(char)
    return (start_row, start_column)

start = find_char(field, 'S')
target = find_char(field, 'X')

plt.imshow(np.array([[c == '#' for c in row] for row in field], dtype=int))

def h(node):
    # Manhattan heuristic
    return abs(target[1] - node[1]) + abs(target[0] - node[0])

def find_neighbors(pos):
    found = []
    for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ind = tuple(np.array(pos) + np.array(d))
        if field[ind[0]][ind[1]] != "#":
            found.append(tuple(np.array(d) + np.array(pos)))
    return found

visited = []
queue = {start: 0 + h(start)}  # node: f-value
while True:
    # pick a node to move forward! this sorts the queue dict by value
    node = sorted(queue, key=queue.get)[0]
    f = queue.pop(node)

    # see if we're finished
    if node == target:
        print(f"Got there in {f} steps")
        break

    # find the neighbors and update their f values
    neighbors = find_neighbors(node)
    g = f - h(node)  # path taken so far
    for n_ in neighbors:
        if n_ in visited:
            continue
        queue[n_] = g + 1 + h(n_)
        visited.append(n_)
