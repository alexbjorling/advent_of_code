import re
import itertools
import multiprocessing

eqs = []
with open("input.txt", "r") as fp:
    for line in fp:
        eqs.append(tuple(map(int, re.findall("\d+", line))))

def check_eqn(eq):
    """
    Returns the test result if there is a combination of operators
    that makes the equation whole. Otherwise zero.
    """
    for operators in itertools.product('+*|', repeat=len(eq)-2):
        res = eq[1]
        for i in range(len(eq) - 2):
            if operators[i] == "+":
                res += eq[i + 2]
            elif operators[i] == "*":
                res *= eq[i + 2]
            else:
                res = int(str(res) + str(eq[i + 2]))
            if res > eq[0]:
                break
        if res == eq[0]:
            return eq[0]
    return 0

with multiprocessing.Pool(12) as pool:
    tot = sum(pool.map(check_eqn, eqs))

assert tot == 61561126043536