import numpy as np

# data
data = np.loadtxt('input.txt', dtype=int)
l1, l2 = data.T
l1 = np.sort(l1)
l2 = np.sort(l2)

# part 1
np.sum(np.abs(l2 - l1)) == 1506483

# part 2
total = 0
for n1 in l1:
    total += n1 * np.sum(l2 == n1)
assert total == 23126924
