import re

with open("input.txt", "r") as fp:
    data = fp.read()

line_length = len(data.split()[0])  # without newline
data = data.replace("\n", " ")      # newline doesn't match . in regex

patterns = [
    "XMAS",  # horizontal
    "X(?=.{%d}M.{%d}A.{%d}S)" % ((line_length,)*3),  # vertical
    "X(?=.{%d}M.{%d}A.{%d}S)" % ((line_length + 1,)*3),  # diagonal 1
    "X(?=.{%d}M.{%d}A.{%d}S)" % ((line_length - 1,)*3),  # diagonal 2
]

tot = 0
for p in patterns:
    tot += len(re.findall(p, data))
    tot += len(re.findall(p, data[::-1]))

assert tot == 2500