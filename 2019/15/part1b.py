"""
Have an ugly solution to find the target node, here we already know it
and do A* to find it, then solve part 2 with a similar loop.
"""

from Intcode import Intcode
import numpy as np
import matplotlib.pyplot as plt; plt.ion()
from copy import deepcopy


## Set up the computer
with open("input.txt", "r") as fp:
    prog = list(map(int, fp.readline().strip().split(",")))

dir_map = {
    1: (-1, 0),
    2: (1, 0),
    3: (0, -1),
    4: (0, 1),
}
inv_dir_map = {v:k for k,v in dir_map.items()}
opposites = {1: 2, 2: 1, 3: 4, 4: 3}

## Do a directed search to find the closest way there. Use the
## Intcode program and keep track of multiple computers.
start = (0, 0)
target = (14, 14)

class Path:
    def __init__(self, computer, target):
        self.history = []
        self.pos = (0, 0)
        self.computer = computer
        self.target = target

    def g(self):
        return(len(self.history))

    def h(self):
        return abs(self.target[1] - self.pos[1]) + abs(self.target[0] - self.pos[0])

    def f(self):
        return self.g() + self.h()

    def possible_moves(self):
        # first find out which moves are possible
        possible_moves = []
        for move in range(1, 5):
            ret = self.computer.run(move)
            if ret == 0:
                # note there's a wall, we haven't moved and we get no new options
                continue
            elif ret > 0:
                # found a possibility, note it and move back
                self.computer.run(opposites[move])
                possible_moves.append(move)
        return possible_moves

    def split(self):
        # return new Path objects from this Path's neighbors
        paths = []
        for move in self.possible_moves():
            p = deepcopy(self)
            p.computer.run(move)
            p.history.append(p.pos)
            p.pos = tuple(np.array(p.pos) + np.array(dir_map[move]))
            paths.append(p)
        return paths

# part 1
visited = []
node0 = Path(Intcode(prog), target)
queue = {node0: node0.f()}  # node: f-value
n = 0
while True:
    n += 1
    if n % 100 == 0:
        print(max([n.g() for n in queue.keys()]))

    # pick a node to move forward! this sorts the queue dict by value
    node = sorted(queue, key=queue.get)[0]
    f = queue.pop(node)

    # see if we're finished
    if node.pos == target:
        print(f"Got there in {f} steps")
        break

    # spawn the node's neighbors
    for new_node in node.split():
        if new_node.pos in visited:
            continue
        queue[new_node] = new_node.f()
        visited.append(new_node.pos)

assert node.g() == 404


# part 2 - start from the previous target node
frontier_nodes = [node,]
next_frontier = []
visited = [node.pos,]
n = -1
while len(frontier_nodes):
    n += 1
    for node in frontier_nodes:
        # split each frontier nodes to cover the neighbours we haven't visited yet
        for new_node in node.split():
            if new_node.pos in visited:
                continue
            next_frontier.append(new_node)
            visited.append(new_node.pos)
    frontier_nodes = next_frontier
    next_frontier = []
print(n)