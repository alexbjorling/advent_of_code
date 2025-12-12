import numpy as np
import re
import sympy
import itertools

# parse an input row to a system of equations A x = b, return (A, b)
def parse(row):
    # read the numbers of the buttons to press
    buttons = re.findall("\\((.*?)\\)", row)
    buttons = [re.findall("([0-9]+)", b) for b in buttons]
    buttons = [list(map(int, b)) for b in buttons]

    # read the sums, ie the joltage levels
    sums = re.findall("\\{(.*?)\\}", row)[0]
    sums = sums.split(",")
    sums = np.array(list(map(int, sums)), dtype=int)

    # convert the button presses to basis vectors
    bases = np.empty((sums.size, len(buttons)), dtype=int)
    for j, b in enumerate(buttons):
        v = np.zeros(len(sums), dtype=int)
        for p in b:
            v[p] += 1
        bases[:, j] = v

    return bases, sums

nrow = -1
with open("input.txt", "r") as fp:
    tot = 0
    for row in fp:
        nrow += 1
        A, b = parse(row)

        # a row-reduced system B x = c with known free variables (not necessarily all integers)
        M = sympy.Matrix(A)
        B, pivots = M.rref()
        rank = len(pivots)
        free = set(range(M.shape[1]))
        [free.remove(i) for i in pivots]
        free = tuple(free)
        _, c = M.rref_rhs(sympy.Matrix(b))

        # a square matrix with the free variables removed, and its inverse
        B = np.array(B).astype(float)[:rank]
        c = np.array(c).astype(float)[:rank].reshape((-1,))
        S = np.hstack([B[:rank, i].reshape(-1, 1) for i in pivots])
        Sinv = np.linalg.inv(S) # turns out S is always the identity...

        # now scan the free variables, move them to the rhs and solve the N x N system
        upper_bound = int(np.max(b))
        best = None
        print(f"row {nrow}: searching rank {rank:2d} problem with {len(free):2d} free parameters on (0, {upper_bound:3d})...")
        for combo in itertools.product(range(upper_bound), repeat=len(free)):
            # construct a new rhs with these values for the free variables
            c_ = np.copy(c)
            for i, ind in enumerate(free):
                base_vec = B[:rank, ind]
                c_ -= combo[i] * base_vec
            # solve the system and see if there's an integer solution
            x = np.dot(Sinv, c_)
            tol = .01
            if np.all((x % 1 < tol) | (x % 1 > (1 - tol))) and np.all(x >= 0):
                # we have a positive integer solution
                presses = np.sum(x) + np.sum(combo)
                best = presses if best is None else min(presses, best)

        if best is not None:
            tot += best
        else:
            raise RuntimeError(f"No solution for row {nrow}")
    print(f"total = {tot}")
    assert(tot == 17424)
