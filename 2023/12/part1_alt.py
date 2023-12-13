import re

def find_solutions(row, *blocks, start=0, blockind=0):
    solutions = []

    if blockind == len(blocks):
        # Done! Stop recursion. Unless we skipped a # somewhere,
        if [len(s) for s in re.findall('(#+)', row)] == list(blocks):
            return [row.replace('?', '.')]
        return []

    # find all positions where the current block could go - stop recursion if there are none
    match = re.search('(?=[^#][?#]{%d}[^#])' % blocks[blockind], row[start:])
    if match is None:
        return []
    pos = start + match.span()[0] + 1

    # evaluate what happens if we do or don't put the block here
    s = row[:pos].replace('?', '.') + '#' * blocks[blockind] + row[pos + blocks[blockind]:]
    solutions += find_solutions(s, *blocks, start=(pos + blocks[blockind]), blockind=blockind+1)
    if row[pos] == '?':
        s = row[:pos].replace('?', '.') + '.' + row[pos + 1:]
        solutions += find_solutions(s, *blocks, start=pos, blockind=blockind)
    return solutions

total = 0
with open('input.txt', 'r') as fp:
    for line in fp:
        row, numbers = re.match('([?.#]+) (.*)', line).groups()
        row = '.' + row + '.'  # pad for regex searching
        numbers = list(map(int, re.findall('([0-9]+)', numbers)))
        solns = find_solutions(row, *numbers)
        total += len(solns)

assert total == 8419
