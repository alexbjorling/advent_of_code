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

# expand the universe
empty_cols = np.where(board.sum(axis=0) == 0)
empty_rows = np.where(board.sum(axis=1) == 0)
for i in empty_rows[::-1]:
	board = np.insert(board, i, 0, axis=0)
for i in empty_cols[::-1]:
	board = np.insert(board, i, 0, axis=1)

# find the distance between the pairs
galaxies = np.array(np.where(board)).T
total = 0
for i in range(galaxies.shape[0]):
	for j in range(i):
		total += np.sum(np.abs(galaxies[i] - galaxies[j]))

assert total == 9723824
