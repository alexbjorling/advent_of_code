"""

For an even number of steps, the possibilities with no rocks are laid out
on a 45-degree rotated sqrt(2) by sqrt(2) grid containing (n+1) by (n+1) points,
spanning 2 * n points horizontally and vertically in the original grid.

For an odd number of steps it's the same, but with the starting point between points:

O.O.O.O.O.O
.O.O.O.O.O.
O.O.OSO.O.O
.O.O.O.O.O.
O.O.O.O.O.O

So in the bulk we can work out the area of the new grid, subsample the rocks on the same grid, and subtract the two.

"""

import numpy as np

# read the data and construct a 3x3 tiled map of obstacles - now ones are rocks
with open('ex.txt', 'r') as fp:
    data = fp.read().strip()
    lines = data.replace('\n', '')
    shape = (len(data.split('\n')), -1)

board = np.copy(np.frombuffer(lines.encode(), dtype=np.uint8).reshape(shape))
start = tuple(map(int, np.where(board == ord('S'))))
M, N = board.shape
assert M == N
board[np.where(board == ord('.'))] = 0
board[np.where(board == ord('#'))] = 1
board[np.where(board == ord('S'))] = 0
board_ = np.copy(board)
board = np.tile(board, (3, 3))
assert start[0] == start[1]
start = start[0] + board.shape[0] // 3

# find a periodic subgrid of rocks
subgrid = []
diagonal = np.array([np.arange(start, -1, -1), np.arange(0, start+1, 1)])
for i in range(start + 1):
    subgrid.append(board[tuple(diagonal + i)])
subgrid = np.array(subgrid, dtype=int)

# the subgrid without rocks would be all the reachable points
reachable_per_subgrid = int(np.prod(subgrid.shape) - subgrid.sum())
print(f'subgrid contains {subgrid.sum()} rocks and {reachable_per_subgrid} reachable points')

subgrid = np.tile(subgrid, (401, 401))  # ok for the example
start = (subgrid.shape[0] - 1) // 2


# 470183123321326 too low
