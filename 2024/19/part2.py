from functools import lru_cache

with open("input.txt", "r") as fp:
    towels, patterns = fp.read().split("\n\n")
    towels = towels.split(", ")
    patterns = patterns.splitlines()

@lru_cache
def search(pattern):
    if len(pattern) == 0:
        return 1

    tot = 0
    for towel in towels:
        n = len(towel)
        if pattern[:n] == towel:
            tot += search(pattern[n:])

    return tot

tot = 0
for p in patterns:
    tot += search(p)

assert tot == 603191454138773