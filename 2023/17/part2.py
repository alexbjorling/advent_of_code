import numpy as np
import queue

ESTIMATED_COST_PER_STEP = 2

class Path:
    """
    Represents a node, including a current position and the last
    consecutive steps which got it done.
    """
    def __init__(self, board, pos=(0,0), vel=(0,1)):
        self.board = board
        self.goal = (board.shape[0] - 1, board.shape[1] - 1)
        self.cost = 0
        self.pos = pos
        self.vel = vel
        self.n_consecutive = 0

    def step(self):
        """
        Return a list of copies for all allowed directions, advanced by one step.
        """

        # pick all allowed directions
        turn_right = [[0, 1],[-1, 0]]
        turn_left = [[0, -1],[1, 0]]
        straight = [[1, 0], [0, 1]]
        if self.n_consecutive < 4:
            turns = [straight]
        elif self.n_consecutive < 10:
            turns = [turn_left, turn_right, straight]
        else:
            turns = [turn_right, turn_left]

        # make branches for each allowed turn
        copies = []
        for turn in turns:
            new_vel = tuple(np.dot(turn, self.vel))
            new_pos = tuple(np.add(self.pos, new_vel))
            # don't fall off the board
            M, N = self.board.shape
            if (new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0]+1 > M or new_pos[1]+1 > N):
                continue
            # otherwise, split of a new path
            clone = self.copy()
            clone.pos = new_pos
            clone.cost += self.board[new_pos]
            clone.vel = new_vel
            if turn is straight:
                clone.n_consecutive += 1
            else:
                clone.n_consecutive = 1
            copies.append(clone)

        return copies

    def copy(self):
        p = Path(self.board)
        p.goal = self.goal
        p.cost = self.cost
        p.pos = self.pos
        p.vel = self.vel
        p.n_consecutive = self.n_consecutive
        return p

    def f(self):
        dist = abs(self.goal[0] - self.pos[0]) + abs(self.goal[1] - self.pos[1])
        return self.cost + ESTIMATED_COST_PER_STEP * dist

    def done(self):
        return (self.pos == self.goal) and (self.n_consecutive >= 4)

    def hash(self):
        return (self.pos, self.vel, self.n_consecutive)

    def __gt__(self, other):
        return self.f() > other.f()


# read the board
board = []
with open('input.txt', 'r') as fp:
    for line in fp:
        board.append([int(s) for s in line.strip()])
board = np.array(board)

# search
cost_map = {}  # map from hashed node to best known cost to get there
q = queue.PriorityQueue()
q.put(Path(board))
while True:
    node = q.get()
    if node.done():
        break

    for new in node.step():
        best_cost = cost_map.get(new.hash(), 99999999)
        if new.cost < best_cost:
            q.put(new)
            cost_map[new.hash()] = new.cost

assert node.cost == 1055
