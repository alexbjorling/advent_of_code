with open("input.txt", "r") as fp:
    towels, patterns = fp.read().split("\n\n")
    towels = towels.split(", ")
    patterns = patterns.splitlines()


# Define a home made caching decorator for fun, would normally
# use functools.lru_cache.
def homemade_cache(func):
    cache = {}
    def call(arg):
        try:
            return cache[arg]
        except KeyError:
            cache[arg] = func(arg)
            return cache[arg]
    return call


# Search through the whole tree of possible towel combinations,
# adding up the number of solutions found.
@homemade_cache
def search(pattern):
    if len(pattern) == 0:
        return 1

    solutions = 0
    for towel in towels:
        n = len(towel)
        if pattern[:n] == towel:
            solutions += search(pattern[n:])
    return solutions


tot = 0
for p in patterns:
    tot += search(p)

assert tot == 603191454138773