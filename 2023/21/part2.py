import numpy as np
import scipy

# read the data and construct a map of obstacles and the current
# state, zero-padded for easier boundaries
with open('input.txt', 'r') as fp:
    data = fp.read().strip()
    lines = data.replace('\n', '')
    shape = (len(data.split('\n')), -1)

board = np.copy(np.frombuffer(lines.encode(), dtype=np.uint8).reshape(shape))
start = np.where(board == ord('S'))[0][0]
board[np.where(board == ord('.'))] = 1
board[np.where(board == ord('#'))] = 0
board[np.where(board == ord('S'))] = 1

# tile to check for periodicity
tiling = 10
M = board.shape[0]
start = start + (tiling - 1) // 2 * board.shape[0]
board = np.tile(board, (tiling, tiling))
current = np.zeros_like(board)
current[start, start] = 1

# an important finding which someone told me about
assert board[start, :].prod() == board[:, start].prod() == 1

# kernel for propagation
kernel = np.array([
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0]])

# main loop
total = []
steps = []
for i in range(board.shape[0]//2-10):
    total.append(current.sum())
    steps.append(i)
    # only convolve the part we need
    n = max(i, 10) + 5
    n1, n2 = start - n, start + n
    current[n1:n2, n1:n2] = scipy.signal.convolve2d(current[n1:n2, n1:n2], kernel, mode='same')
    current[:] = np.where(current > 0, 1, 0)
    current[n1:n2] = current[n1:n2] * board[n1:n2]

# another important finding I heard about is that there's various
# periodicities, where N(n) is exactly quadratic (as it of course
# is on average).
#
# One which is commensurate with the target number of steps, which
# means that (NN-65)/131 is an integer and that we should look at
# periods when we stand on the edge of the board
points = 65, 65+M, 65+2*M
steps = np.array(steps)
total = np.array(total)
x = [steps[i] for i in points]
y = [total[i] for i in points]
d = np.polyfit(x, y, 2)
assert int(round(d[0] * (65+3*M)**2 + d[1] * (65+3*M) + d[2])) == total[65+3*M]

NN = 26501365
# floor here because we see the decimal increasing continuously in the extrapolation
assert np.floor(d[0] * NN**2 + d[1] * NN + d[2]) == 620962518745459
