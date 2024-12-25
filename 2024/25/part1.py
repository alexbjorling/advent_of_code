import numpy as np

# load the data as an array of ascii values
locks, keys = [], []
with open("input.txt", "r") as fp:
    for block in fp.read().split("\n\n"):
        arr = []
        for row in block.split():
            arr.append([ord(c) for c in row.strip()])
        arr = np.array(arr)
        arr[np.where(arr == ord("#"))] = 1
        arr[np.where(arr == ord("."))] = 0
        height = arr.shape[0]
        if np.all(arr[0, :] == 1):
            locks.append(np.sum(arr, 0))
        else:
            keys.append(np.sum(arr, 0))

tot = 0
for key in keys:
    for lock in locks:
        if np.all(key + lock <= height):
            tot += 1
print(tot)
assert tot == 3619