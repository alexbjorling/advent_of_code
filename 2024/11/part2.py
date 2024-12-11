import numpy as np
from functools import cache
import multiprocessing

"""
Horrendous solution which runs in 100 seconds:

1. make a cached function to evolve a number to the next generation
2. make a cached function which evolves a number over 25 generations
3. in parallel, for each of the 8 starting numbers:
    - evolve the number 25 generations
    - evolve each of those 25 generations
    - evolve each of those 25 generations and measure the length
"""

# load the data
with open("input.txt", "r") as fp:
    data = [int(c) for c in fp.read().strip().split()]

@cache
def expand(s):
    """
    Take a single number and expand it to a list of length one or two
    """
    if s == 0:
        return [1,]

    length = int(np.floor(np.log10(s))) + 1
    if length % 2 == 0:
        half = length // 2
        s_ = str(s)
        return [int(s_[:half]), int(s_[half:])]
    else:
        return [s * 2024,]

@cache
def evolve25(num):

    nums = [num,]
    for i in range(25):
        new_data = []
        for s in nums:
            new_data += expand(s)
        nums = new_data
    return nums

import time
t0 = time.time()

def wrap(s):
    tot = 0
    for s1 in evolve25(s):
        for s2 in evolve25(s1):
            tot += len(evolve25(s2))
    return tot

with multiprocessing.Pool(len(data)) as pool:
    tot = sum(pool.map(wrap, data))

print(time.time() - t0)
assert tot == 284973560658514
