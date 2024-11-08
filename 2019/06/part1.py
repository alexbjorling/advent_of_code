# load data
orbits = {}
with open("input.txt", "r") as fp:
    for line in fp:
        a, b = line.strip().split(")")
        orbits[b] = a

# each object except COM orbits exactly one other object,
# so we can count based on the keys of orbits.
total = 0
for k in orbits.keys():
    # now count all the orbits of this object
    k_ = k
    while k_ != "COM":
        total += 1
        k_ = orbits[k_]

assert total == 158090