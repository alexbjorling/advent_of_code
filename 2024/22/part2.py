import numpy as np
import time; t0 = time.time()

with open("input.txt", "r") as fp:
    data = list(map(int, fp.read().splitlines()))

def prune(num):
    # keep the last 24 bits
    return num % 16777216

def mix(num, new):
    # xor
    return num ^ new

def generate(num):
    num = prune(mix(num, num * 64))
    num = prune(mix(num, num // 32))
    num = prune(mix(num, num * 2048))
    return num

def price_list(num, n):
    ret = []
    for i in range(n):
        ret.append(int(str(num)[-1]))
        num = generate(num)
    return ret

# make numpy arrays of prices and changes, as (number, buyer)
print("generating tables...")
prices = np.empty((2000, len(data)), dtype=int)
deltas = np.empty((2000, len(data)), dtype=int)
for i in range(len(data)):
    prices[:, i] = price_list(data[i], 2000)
deltas[1:, :] = np.diff(prices, axis=0)

# loop over the number sequences backwards, to find the buyers' price for each sequence encountered
print("indexing buyers' 4-tuple sequences...")
gains = [{} for i in range(len(data))]
for i in range(2000-1, 4, -1):  # exclude first row which is garbage
    for j in range(len(data)):
        seq = tuple(deltas[i-4:i, j])
        try:
            gains[j][seq] = prices[i-1, j]
        except:
            continue

# find all the sequences we have
print("listing all the sequences...")
sequences = set()
for g in gains:
    sequences = sequences.union(set(g.keys()))

# see which earns the most
print("comparing all sequences across buyers...")
options = []
for seq in sequences:
    earnings = 0
    for g in gains:
        earnings += g.get(seq, 0)
    options.append(earnings)

print(f"done! brute forced this in {time.time()-t0:.1f} seconds")
assert max(options) == 2152
