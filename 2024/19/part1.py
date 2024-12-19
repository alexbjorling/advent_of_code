with open("input.txt", "r") as fp:
    towels, patterns = fp.read().split("\n\n")
    towels = towels.split(", ")
    patterns = patterns.splitlines()

# Find any solution, by returning 1 as soon as we reach the end of the string.
def search(pattern):
    if len(pattern) == 0:
        return 1

    solved = 0
    for towel in towels:
        n = len(towel)
        if pattern[:n] == towel:
            if search(pattern[n:]):
                return 1
    return solved

tot = 0
for p in patterns:
    tot += search(p)

assert tot == 216