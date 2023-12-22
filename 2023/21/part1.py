import numpy as np
import scipy

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

# kernel for propagation
kernel = np.array([
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0]])

# main loop
for i in range(64):
    current[:] = scipy.signal.convolve2d(current, kernel, mode='same')
    current[:] = np.where(current > 0, 1, 0)
    current[:] = current * board

assert current.sum() == 3740
