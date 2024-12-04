import re
import numpy as np

data = []
with open("input.txt", "r") as fp:
    for line in fp:
        data.append(line.strip())

tot = 0
length = len(data[0].strip())  # without newline
data = ' '.join(data)          # space instead of newline, to match . in regex

patterns = [
    # four rotations of the cross
    "M(?=.M.{%d}A.{%d}S.S)" % ((length-1,)*2),
    "M(?=.S.{%d}A.{%d}M.S)" % ((length-1,)*2),
    "S(?=.S.{%d}A.{%d}M.M)" % ((length-1,)*2),
    "S(?=.M.{%d}A.{%d}S.M)" % ((length-1,)*2),
]

for p in patterns:
    tot += len(re.findall(p, data))

assert tot == 1933