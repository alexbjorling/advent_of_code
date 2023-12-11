import numpy as np
import re

# read input
with open('input.txt', 'r') as fp:
	indata = fp.read().strip().split()

# convert to array
board = np.zeros((len(indata), len(indata[0])), dtype=int)
for i in range(len(indata)):
	for it in re.finditer('\#', indata[i]):
		board[i, it.span()[0]] = 1

# find empty rows
empty_cols = np.where(board.sum(axis=0) == 0)[0]
empty_rows = np.where(board.sum(axis=1) == 0)[0]

# keep a sparse list of galaxies and expand their coordinates
galaxies = np.array(np.where(board)).T
for i in range(galaxies.shape[0]):
	galaxies[i, 0] += sum(galaxies[i, 0] > empty_rows) * (1000000 - 1)
	galaxies[i, 1] += sum(galaxies[i, 1] > empty_cols) * (1000000 - 1)

# sum up their distances
total = 0
for i in range(galaxies.shape[0]):
	for j in range(i):
		total += np.sum(np.abs(galaxies[i] - galaxies[j]))

assert total == 731244261352
