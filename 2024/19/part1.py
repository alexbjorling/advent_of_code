with open("input.txt", "r") as fp:
    towels, patterns = fp.read().split("\n\n")
    towels = towels.split(", ")
    patterns = patterns.splitlines()

def search(pattern):
    if len(pattern) == 0:
        return 1

    tot = 0
    for towel in towels:
        n = len(towel)
        if pattern[:n] == towel:
            tot += search(pattern[n:])
            if tot:  # bail early if we find a solution
                return tot

    return tot

tot = 0
for p in patterns:
    if search(p):
        tot += 1

assert tot == 216