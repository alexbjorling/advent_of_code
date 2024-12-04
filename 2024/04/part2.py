import re

with open("input.txt", "r") as fp:
    data = fp.read()

line_length = len(data.split()[0])  # without newline
data = data.replace("\n", " ")      # newline doesn't match . in regex

patterns = [
    # four rotations of the cross
    "M(?=.M.{%d}A.{%d}S.S)" % ((line_length-1,)*2),
    "M(?=.S.{%d}A.{%d}M.S)" % ((line_length-1,)*2),
    "S(?=.S.{%d}A.{%d}M.M)" % ((line_length-1,)*2),
    "S(?=.M.{%d}A.{%d}S.M)" % ((line_length-1,)*2),
]

tot = 0
for p in patterns:
    tot += len(re.findall(p, data))

assert tot == 1933