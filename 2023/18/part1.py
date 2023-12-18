import numpy as np
import sys
sys.setrecursionlimit(100000)  # :)

# read all the steps and embed the loop in an array with a margin
dir_map = {'R': np.array((0, 1)), 'L': np.array((0, -1)), 'U': np.array((-1, 0)), 'D': np.array((1, 0))}
loop = []
pos = np.array((-2, -2))
with open('input.txt', 'r') as fp:
    for line in fp:
        direction = dir_map[line.split()[0]]
        length = int(line.split()[1])
        for i in range(length):
            pos = pos + direction
            loop.append(pos)
loop = np.array(loop) - np.min(loop, axis=0) + 1
M, N = np.max(loop, axis=0) + 1
data = np.zeros((M + 2, N + 2), dtype=np.uint8)
data[(loop[:, 0], loop[:, 1])] = 1

# render a nice data plot
def nice(arr):
    M, N = arr.shape
    nice_data = np.ones((M, N + 1), dtype=np.uint8) * ord('.')
    nice_data[np.where(arr)] = ord('#')
    nice_data[:, -1] = ord('\n')
    return nice_data.tobytes().decode()

# flood fill
def flood(data, pos):
    if data[pos]:
        return
    data[pos] = 1
    flood(data, (pos[0], pos[1]+1))
    flood(data, (pos[0], pos[1]-1))
    flood(data, (pos[0]+1, pos[1]))
    flood(data, (pos[0]-1, pos[1]))

# flood fill in place
start = (M//2,N//2)
flood(data, start)
assert np.sum(data) == 39039
