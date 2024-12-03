import re

data = []
with open ('input.txt', 'r') as fp:
    for line in fp:
        data.append(line.strip())
    data = ''.join(data)

tot = 0
do = True
pattern = "mul\(([0-9]{1,3}),([0-9]{1,3})\)" + "|" + "(do\(\))" + "|" + "(don't\(\))"
for match in re.finditer(pattern, data):
    if match.group() == "do()":
        do = True
    elif match.group() == "don't()":
        do = False
    elif do:
        tot += int(match.groups()[0]) * int(match.groups()[1])

assert tot == 98729041