"""
Solution after looking at the real answer (Calle's).
"""

# load the data
with open("input.txt", "r") as fp:
    data = [int(c) for c in fp.read().strip().split()]

# helper function, expands n -> [n1, n2] or [n1,]
def expand(s):
    """
    Take a single number and expand it to a list of length one or two
    """
    if s == 0:
        return [1,]

    length = len(str(s))
    if length % 2 == 0:
        half = length // 2
        s_ = str(s)
        return [int(s_[:half]), int(s_[half:])]
    else:
        return [s * 2024,]

# act only on unique stone types, the order doesn't matter
data = {d:1 for d in data}
for i in range(75):
    new_data = {}
    for k, v in data.items():
        for new_val in expand(k):
            new_data[new_val] = new_data.get(new_val, 0) + v
    data = new_data

assert sum(data.values()) == 284973560658514
