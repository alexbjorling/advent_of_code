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
    "XMAS",  # horizontal
    "X(?=.{%d}M.{%d}A.{%d}S)" % ((length,)*3),  # vertical
    "X(?=.{%d}M.{%d}A.{%d}S)" % ((length + 1,)*3),  # diagonal 1
    "X(?=.{%d}M.{%d}A.{%d}S)" % ((length - 1,)*3),  # diagonal 2
]

for p in patterns:
    tot += len(re.findall(p, data))
    tot += len(re.findall(p, data[::-1]))

assert tot == 2500