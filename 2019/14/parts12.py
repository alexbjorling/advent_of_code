import re
import numpy as np

class Reaction:
    def __init__(self, react, prod):
        self.prod = prod
        self.react = react

reactions = {}
with open("input.txt", "r") as fp:
    for line in fp:
        react, prod = line.strip().split("=>")

        # regex out the individual reactants and products e.g. [('7', 'A'), ('1', 'E')]
        expr = "[\s]*([\d]+)[\s]*([A-Z]+)"
        react = re.findall(expr, react)
        prod = re.findall(expr, prod)
        assert len(prod) == 1  # assuming single reactant

        # clean up the integers
        react = [(int(p[0]), p[1]) for p in react]
        prod = [(int(p[0]), p[1]) for p in prod]

        # store those as Reaction objects, with the single product as key
        reactions[prod[0][1]] = Reaction(react, prod)


def make_fuel(reactions, n):
    """
    Calculate how many ORE we need to make n FUEL.
    """

    # Keep a wishlist of things we need, and update it by running
    # reactions backwards to see what we need. Negative numbers means
    # we have stuff left over.
    wishlist = {"FUEL": n}
    while True:
        # work out how to update the wishlist
        updates = {}
        for prod, wanted in wishlist.items():
            if prod == "ORE":  # can't make ORE
                continue
            # how many prod:s does the reaction make
            provided = reactions[prod].prod[0][0]
            # so how many times should we run the reaction?
            mult = int(np.ceil(wanted / provided))
            # remove the product from the wishlist, and add the reactants instead
            updates[prod] = updates.get(prod, 0) - mult * provided
            for n, r in reactions[prod].react:
                updates[r] = updates.get(r, 0) + n * mult

        # do the wishlist update
        for k, v in updates.items():
            wishlist[k] = wishlist.get(k, 0) + v

        # are we done?
        remaining = [k for k, v in wishlist.items() if v > 0]
        if remaining == ["ORE"]:
            return wishlist["ORE"]

# part 1
ore_per_fuel = make_fuel(reactions, 1)
assert ore_per_fuel == 751038

# part 2 - find n for which make_fuel(n) <= N but make_fuel(n+1) > N
N = int(1e12)

# first, we'll find two numbers n1 <= n <= n2 to contain the number we're after (assume inclusive to be safe)
n1 = 0; n2 = ore_per_fuel
while make_fuel(reactions, n2) < N:
    n1 = n2
    n2 += ore_per_fuel

# then, we can bisect the interval [n1, n2] to find our n.
while n2 - n1 > 1:
    mid = n1 + (n2 - n1) // 2
    if make_fuel(reactions, mid) > N:
        n2 = mid
    else:
        n1 = mid

answer = n1 if make_fuel(reactions, n2) > N else n2
assert answer == 2074843
