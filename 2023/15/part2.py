import re

with open('input.txt', 'r') as fp:
    line = fp.read().strip()

def hash(string):
    current = 0
    for l in string:
        current += ord(l)
        current *= 17
        current %= 256
    return current

lens_lookup = {}  # map from lens id to focal length
boxes = [[] for i in range(256)]

for string in line.split(','):
    match = re.match('(.*)=([0-9]+)', string)
    if match is not None:
        lens, strength = match.groups()
        lens_lookup[lens] = int(strength)
        box = boxes[hash(lens)]
        if lens not in box:
            box.append(lens)
    else:
        lens = string[:-1]
        box = boxes[hash(lens)]
        if lens in box:
            box.remove(lens)

# sum up 
total = 0
for i in range(len(boxes)):
    for j in range(len(boxes[i])):
        total += (i + 1) * (j + 1) * lens_lookup[boxes[i][j]]

assert total == 261505
