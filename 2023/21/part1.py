import numpy as np

# read the data and construct a map of obstacles and the current
# state, zero-padded for easier boundaries
with open('input.txt', 'r') as fp:
    data = fp.read().strip()
    lines = data.replace('\n', '')
    shape = (len(data.split('\n')), -1)

board = np.copy(np.frombuffer(lines.encode(), dtype=np.uint8).reshape(shape))
board = np.pad(board, 1)
start = tuple(map(int, np.where(board == ord('S'))))
current = np.zeros_like(board)
current[start] = 1
board[np.where(board == ord('.'))] = 1
board[np.where(board == ord('#'))] = 0
board[start] = 1

# update the current state 64 times
deltas = np.array([(1, 0), (-1, 0), (0, 1), (0, -1)])
for i in range(64):
    starting_points = np.array(np.where(current)).T
    current[:] = 0
    for start in starting_points:
        for delta in deltas:
            new = tuple(start + delta)
            current[new] = board[new]

assert current.sum() == 3740
