import numpy as np
import scipy
import matplotlib.pyplot as plt

# read the data and construct a map of obstacles and the current
# state, zero-padded for easier boundaries
with open('ex.txt', 'r') as fp:
    data = fp.read().strip()
    lines = data.replace('\n', '')
    shape = (len(data.split('\n')), -1)

board = np.copy(np.frombuffer(lines.encode(), dtype=np.uint8).reshape(shape))
start = tuple(map(int, np.where(board == ord('S'))))
board[np.where(board == ord('.'))] = 1
board[np.where(board == ord('#'))] = 0
board[start] = 1
board_ = np.copy(board)
M, N = board.shape

# tile and check for periodicity
tiling = 7
start = (start[0] + (tiling - 1) // 2 * board.shape[0],) * 2
board = np.tile(board, (tiling, tiling))

# set the starting state
current = np.zeros_like(board)
updated = np.copy(current)
current[start] = 1

# nine types of unit cell:
# * the central one where the front starts in the center
# * four edge ones where the peak of the rhomb hits on the edge
# * four corner ones where the moving front hits a corner
# keep track of their evolution as function of steps:
central, edge, corner = [], [], []

# create some views
c = start[0]
frame = (M-1) // 2  # pixels between start and edge
right = bottom = c + 1 + frame
left = top = c - frame
views = {
    'central': current[top:bottom, left:right],
    'edge_r': current[top:bottom, right:right+M],
    'edge_b': current[bottom:bottom+M, left:right],
    'edge_l': current[top:bottom, left-M:left],
    'edge_t': current[top-M:top, left:right],
    'corner_ur': current[top-M:top, right:right+M],
    'corner_br': current[bottom:bottom+M, right:right+M],
    'corner_bl': current[bottom:bottom+M, left-M:left],
    'corner_ul': current[top-M:top, left-M:left],
}

total = {k:[] for k in views.keys()}

# propagate the board and measure the different unit cell types
kernel = np.array([
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0]])

for i in range(4*M):
    for k in total.keys():
        total[k].append(views[k].sum())

    current[:] = scipy.signal.convolve2d(current, kernel, mode='same')
    current[:] = np.where(current > 0, 1, 0)
    current[:] = current * board

plt.figure()
for k, v in total.items():
    plt.plot(v, label=k)
plt.legend()

# so full cells have this amount of positions (since we're looking at odd steps)
# and they are different depending on cell type because of some odd/even shift
full = {k: v[4*M-1] for k, v in total.items()}

# now look at the actual question
n = 1000
total = 0

# add up the edge cells (along the x and y axes)
steps_to_cell_edge = (M - 1) // 2               # after this number of steps + 1 we are in the next cell
corner = (n + steps_to_cell_edge) // M    # this is the unit cell number on the corners (center is 0)
edge_cells = [(0, corner), (0, -corner), (corner, 0), (-corner, 0)]  # these are the cells on the corners of the rhomb that get hit on the edge


# center cell
if corner:
    total += full['central']
    # four rows of full vertical and horizontal cells from 1 to corner-1
    total += (corner - 1) * (full['bottom'] + full['top'] + full['left'] + full['right'])
    # the actual corner cells
    ...
else:
    # just account for the central box and nothing else
    ...


# now just work out what unit cells are on the moving front, and add up their
# time evolutions depending on type, with the appropriate time offsets.
