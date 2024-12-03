import re

data = []
with open ('input.txt', 'r') as fp:
    for line in fp:
        data.append(line.strip())
    data = ''.join(data)

factors = re.findall("mul\(([0-9]{1,3}),([0-9]{1,3})\)", data)
tot = 0
for fac in factors:
    tot += int(fac[0]) * int(fac[1])

assert tot == 181345830