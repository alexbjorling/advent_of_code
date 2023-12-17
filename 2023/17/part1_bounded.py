import numpy as np


class BoundedSearcher(object):
    """
    Bounded search with the diagonal zigzag as first estimate of the
    bound. Seems to work, but too slow.
    """
    def __init__(self, board):
        self.board = board

        # estimate bound by going diagonally to the goal
        self.bound = 0
        self.best_trajectory = None
        assert np.allclose(*self.board.shape)
        i, j = 0, 0
        while (i+1, j+1) != self.board.shape:
            i += 1
            self.bound += self.board[i, j]
            j += 1
            self.bound += self.board[i, j]
        print('initial bound is', self.bound)
        self.full_history = []

    def search(self, pos, vel, trajectory=[], cost=0, n_straight=0):
#        trajectory.append(pos)

        # are we there yet?
        M, N = self.board.shape
        if pos == (M-1, N-1):
            if cost < self.bound:
                self.bound = cost
                self.best_trajectory = trajectory
                print('found path, bound =', cost)
            return

        # ok, should we continue or are we out of bounds?
        expected_cost_per_step = 3 # self.board.min()  # super conservative
        if cost + expected_cost_per_step * (M - pos[0] + N - pos[1]) > self.bound:
            return

        # search more
        vels = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        np.random.shuffle(vels)
        for new_vel in vels:
            new_pos = tuple(np.add(pos, new_vel))
            is_straight = (new_vel == vel)
            # can't go backwards
            if (-vel[0], -vel[1]) == new_vel:
                continue
            # skip forward direction if we've taken 3 already
            if is_straight and n_straight == 3:
                continue
            # don't fall off the board
            if (new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0]+1 > M or new_pos[1]+1 > N):
                continue
            # otherwise, ready to recurse!
            traj_copy = trajectory[:]
            self.search(new_pos, new_vel, traj_copy, cost+self.board[new_pos], (n_straight+1 if is_straight else 1))

board = []
with open('ex.txt', 'r') as fp:
    for line in fp:
        board.append([int(s) for s in line.strip()])
board = np.array(board)
searcher = BoundedSearcher(board)
searcher.search(pos=(0,0), vel=(0,1))

# visualize and print the total cost
vis = np.ones((len(board), len(board[0])+1), dtype='uint8') * ord('-')
total = 0
for i,j in searcher.best_trajectory:
    total += board[i][j]
    vis[i, j] = ord(str(board[i][j]))
vis[:, -1] = ord('\n')
total -= board[0][0]  # doesn't count
print(vis.tobytes().decode(), '=', total)
