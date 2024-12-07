import re
import itertools

eqs = []
with open("input.txt", "r") as fp:
    for line in fp:
        eqs.append(tuple(map(int, re.findall("\d+", line))))

tot = 0
for eq in eqs:
    for operators in itertools.product('+*|', repeat=len(eq)-2):
        res = eq[1]
        for i in range(len(eq) - 2):
            if operators[i] == "+":
                res += eq[i + 2]
            elif operators[i] == "*":
                res *= eq[i + 2]
            else:
                res = int(str(res) + str(eq[i + 2]))
        if res == eq[0]:
            tot += eq[0]
            break

assert tot == 61561126043536