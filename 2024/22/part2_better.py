import numpy as np
import time; t0 = time.time()
from collections import defaultdict

with open("input.txt", "r") as fp:
    data = list(map(int, fp.read().splitlines()))

def price_list(num, n):
    for i in range(n):
        yield num % 10
        num = (num ^ (num << 6)) % 16777216
        num = (num ^ (num >> 5)) % 16777216
        num = (num ^ (num << 11)) % 16777216

earnings = defaultdict(int)
for buyer in data:
    seen_sequences = set()
    prices = list(price_list(buyer, 2000))
    diff = np.diff(prices)
    for i in range(3, len(diff)):
        key = tuple(diff[i-3:i+1])
        if key in seen_sequences:
            continue
        seen_sequences.add(key)
        earnings[key] += prices[i + 1]

rev = {v: k for k, v in earnings.items()}
best = max(earnings.values())
assert best == 2152

print(f"done! brute forced this in {time.time()-t0:.1f} seconds")
