import numpy as np

class Propagator(object):
    def __init__(self, board):
        self.board = board
        self.done = []

    def propagate(self, pos, vel):

        # detect loops, quit if any branch has been here
        if (pos, vel) in self.done:
            return []
        self.done.append((pos, vel))

        # stop recursion when we fall off the board
        if min(pos) < 0 or pos[0]+1 > len(self.board) or pos[1]+1 > len(self.board[0]):
            return []

        square = self.board[pos[0]][pos[1]]

        # 2 by 2 matrices for turning right and left
        turn_right = [[0, 1],[-1, 0]]
        turn_left = [[0, -1],[1, 0]]
        horizontal = bool(vel[1])

        history = [pos,]

        # evaluate the next step(s)
        if square == '.':
            history += self.propagate((pos[0]+vel[0], pos[1]+vel[1]), vel)
        elif square in '/\\':
            if square == '/':
                rotation = turn_left if horizontal else turn_right
            else:
                rotation = turn_right if horizontal else turn_left
            vel = tuple(np.dot(rotation, vel))
            history += self.propagate((pos[0]+vel[0], pos[1]+vel[1]), vel)
        elif square in '|-':
            if (horizontal and square == '-') or (not horizontal and square == '|'):
                # pass through
                history += self.propagate((pos[0]+vel[0], pos[1]+vel[1]), vel)
            else:
                # split
                old_vel = vel
                vel = tuple(np.dot(turn_left, old_vel))
                history += self.propagate((pos[0]+vel[0], pos[1]+vel[1]), vel)
                vel = tuple(np.dot(turn_right, old_vel))
                history += self.propagate((pos[0]+vel[0], pos[1]+vel[1]), vel)

        return history

with open('input.txt', 'r') as fp:
    board = fp.read().strip().split()

p = Propagator(board)
h = p.propagate((0, 0), (0, 1))
assert len(set(h)) == 6816
