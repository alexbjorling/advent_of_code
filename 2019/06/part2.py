# load data
orbits = {}
with open("input.txt", "r") as fp:
    for line in fp:
        a, b = line.strip().split(")")
        orbits[b] = a


def count_steps(start, stop):
    total = 0
    k_ = start
    while k_ != stop:
        total += 1
        k_ = orbits[k_]
    return total


def list_parents(child):
    parents = []
    k_ = child
    while k_ != "COM":
        parents.append(k_)
        k_ = orbits[k_]
    parents.append("COM")
    return parents


# find the first common parent
n1 = orbits["YOU"]
n2 = orbits["SAN"]
p1 = list_parents(n1)
p2 = list_parents(n2)
for p_ in p1:
    if p_ in p2:
        common_parent = p_
        break

# count the steps from n1 -> common_parent -> n2
tot = count_steps(n1, common_parent) + count_steps(n2, common_parent)
assert tot == 241
