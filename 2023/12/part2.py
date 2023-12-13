import re
from functools import lru_cache

@lru_cache(maxsize=None)
def find_solutions(row, *blocks):
    solutions = 0

    if len(blocks) == 0:
        # done! make sure there are no #:s we haven't seen yet
        return 1 if not '#' in row else 0

    # find all positions where the current block could go - stop recursion if there are none
    match = re.search('(?=[^#][?#]{%d}[^#])' % blocks[0], row)
    if match is None:
        return 0
    pos = match.span()[0] + 1
    if '#' in row[:pos]:  # make sure we don't rush past any #:s
        return 0

    # evaluate what happens if we do or don't put the block here
    solutions += find_solutions(row[pos + blocks[0]:], *blocks[1:])
    if row[pos] == '?':
        solutions += find_solutions('.' + row[pos + 1:], *blocks)
    return solutions

total = 0
with open('input.txt', 'r') as fp:
    for line in fp:
        row, numbers = re.match('([?.#]+) (.*)', line).groups()
        numbers = list(map(int, re.findall('([0-9]+)', numbers)))
        row = (row + '?') * 4 + row
        row = '.' + row + '.'  # pad for regex searchings
        numbers = 5 * numbers
        total += find_solutions(row, *numbers)

assert total == 160500973317706
