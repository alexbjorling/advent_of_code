import numpy as np
import time

HEURISTIC = 4

class Path(object):
    """
    Represents a unique path, including a current position and how it
    got there. Has knowledge of the board too and can branch itself.
    """
    def __init__(self, board):
        self.board = board
        self.goal = (board.shape[0] - 1, board.shape[1] - 1)
        self.cost = 0  # redundant but nice
        self.history = [(0,0)]

    def step(self):
        """
        Return a list of copies for all allowed directions, advanced by one step.
        """

        # have we already taken 3 steps in the same direction?
        must_turn = False
        if max(np.abs(np.diff(self.history[-4:], axis=0).sum(axis=0))) == 3:
            must_turn = True

        # find the direction we came from
        if len(self.history) == 1:
            vel = (0, 1)  # starting direction
        else:
            vel = tuple(np.subtract(self.history[-1], self.history[-2]))

        # pick all allowed directions
        vels = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        copies = []
        for new_vel in vels:
            # don't go forward if we're not allowed
            if must_turn and (new_vel == vel):
                continue
            # never go backward
            if (-vel[0], -vel[1]) == new_vel:
                continue
            new_pos = tuple(np.add(self.history[-1], new_vel))
            # don't fall off the board
            M, N = self.board.shape
            if (new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0]+1 > M or new_pos[1]+1 > N):
                continue
            # otherwise, split of a new path
            clone = self.copy()
            clone.history.append(new_pos)
            clone.cost += self.board[new_pos]
            copies.append(clone)

        return copies

    @property
    def node(self):
        return tuple(self.history[-4:])

    def copy(self):
        p = Path(self.board)
        p.goal = self.goal
        p.cost = self.cost
        p.history = self.history[-4:]  # copy
        return p

    def g(self):
        return self.cost

    def h(self):
        pos = self.history[-1]
        dist = self.goal[0] - pos[0] + self.goal[1] - pos[1]
        return dist * HEURISTIC

    def f(self):
        return self.g() + self.h()

    def there(self):
        return self.history[-1] == self.goal

    def __gt__(self, other):
        return self.f() > other.f()


# read the board
board = []
with open('input.txt', 'r') as fp:
    for line in fp:
        board.append([int(s) for s in line.strip()])
board = np.array(board)

# search
t0 = time.time()
t1 = t0
current_min = 1
start = Path(board)
cost_map = {current_min: [start]}  # map from estimated total cost to list of Path objects
node_map = {start.node: start}  # map from phase space (history[-4:]) to path object

i = 0
while True:
    # grab the first path with the best f() and propagate
    best = cost_map[current_min].pop()
    node_map.pop(best.node)
    if best.there():
        break
    new_cost_map = best.step()

    # handle the new cost_map, sort them into the two dicts
    for new in new_cost_map:

        # do we already have a path with this phase space position? is so, only keep the best one
        if new.node in node_map:
            # we have a node at this phase space position
            old = node_map[new.node]
            if new.f() < old.f():
                # the new one is better
                if new.f() not in cost_map.keys():
                    cost_map[new.f()] = []
                cost_map[new.f()].append(new)
                cost_map[old.f()].remove(old)
                node_map[new.node] = new
            else:
                # the old one is better
                continue
        else:
            if new.f() not in cost_map.keys():
                cost_map[new.f()] = []
            cost_map[new.f()].append(new)
            node_map[new.node] = new

    # remove empty lists when needed
    if not cost_map[current_min]:
        cost_map.pop(current_min)
    current_min = min(cost_map.keys())

    if i % 10000 == 0:
        total = sum([len(l) for l in cost_map.values()])
        print(f'{i:010d} ({time.time()-t1:.1f} s), {len(cost_map): 5d} tiers, best is {current_min: 4d} and worst is {max(cost_map.keys()): 4d}, storing {total} paths.')
        t1 = time.time()
    i += 1
t = time.time() - t0

# visualize and print the total cost
vis = np.ones((len(board), len(board[0])+1), dtype='uint8') * ord('-')
total = 0
for ii,jj in best.history:
    total += board[ii][jj]
    vis[ii, jj] = ord(str(board[ii][jj]))
vis[:, -1] = ord('\n')
total -= board[0][0]  # doesn't count
print(vis.tobytes().decode().strip())
print(f'= {best.cost}, used {i} iterations and took {t:.2f} s')
