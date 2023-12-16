"""
Trying with caching which speeds things up a lot, but it's hard
because of the combination of loops and branching. It's not as
simple as caching, because the cached trajectory might have been
terminated because of a loop. On the other hand, we can't just
fast-forward and continue cached runs, because they can contain
branches and we'd have to keep track of all the tips.
"""

import numpy as np

class Propagator(object):
    def __init__(self, board):
        self.board = board
        self.visited = []  # list of (pos, vel) points we've been at

    def propagate(self, state, clear=False):

        if clear:
            self.visited = []

        # stop recursion when we fall off the board
        pos, vel = state
        if min(pos) < 0 or pos[0]+1 > len(self.board) or pos[1]+1 > len(self.board[0]):
            return []

        # detect loops, quit if any branch has been here
        if state in self.visited:
            return []
        self.visited.append(state)

        history = [state,]

        square = self.board[pos[0]][pos[1]]

        # 2 by 2 matrices for turning right and left
        turn_right = [[0, 1],[-1, 0]]
        turn_left = [[0, -1],[1, 0]]
        horizontal = bool(vel[1])

        # evaluate the next step(s)
        if square == '.':
            state = ((pos[0]+vel[0], pos[1]+vel[1]), vel)
            res = self.propagate(state)
            history += res
        elif square in '/\\':
            if square == '/':
                rotation = turn_left if horizontal else turn_right
            else:
                rotation = turn_right if horizontal else turn_left
            vel = tuple(np.dot(rotation, vel))
            state = ((pos[0]+vel[0], pos[1]+vel[1]), vel)
            res = self.propagate(state)
            history += res
        elif square in '|-':
            if (horizontal and square == '-') or (not horizontal and square == '|'):
                # pass through
                state = ((pos[0]+vel[0], pos[1]+vel[1]), vel)
                res = self.propagate(state)
                history += res
            else:
                # split
                old_vel = vel

                vel = tuple(np.dot(turn_left, old_vel))
                state = ((pos[0]+vel[0], pos[1]+vel[1]), vel)
                res = self.propagate(state)
                history += res

                vel = tuple(np.dot(turn_right, old_vel))
                state = ((pos[0]+vel[0], pos[1]+vel[1]), vel)
                res = self.propagate(state)
                history += res

        return history

with open('input.txt', 'r') as fp:
    board = fp.read().strip().split()

coverage = []
M, N = len(board), len(board[0])
p = Propagator(board)
for i in range(M):
    print(i)
    traj = p.propagate(((i, 0), (0, 1)), clear=True)
    coverage.append(len(set([state[0] for state in traj])))
    traj = p.propagate(((i, N-1), (0, -1)), clear=True)
    coverage.append(len(set([state[0] for state in traj])))
for j in range(N):
    print(j)
    traj = p.propagate(((0, j), (1, 0)), clear=True)
    coverage.append(len(set([state[0] for state in traj])))
    traj = p.propagate(((M-1, j), (-1, 0)), clear=True)
    coverage.append(len(set([state[0] for state in traj])))

assert max(coverage) == 8163
