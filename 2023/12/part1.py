import re

def find_solutions(row, blocks, start=0, blockind=0):
    solutions = []
    for pos in range(start, len(row) - blocks[blockind] + 1):
        # is this block position consistent with the row?
        allowed = row[pos:pos+blocks[blockind]].replace('#', '?') == '?' * blocks[blockind]
        collision = row[pos+blocks[blockind]:].startswith('#') or ((pos > 0) and row[pos-1] == '#')
        if allowed and not collision:
            # it could or should go here - make a string so far and call on the rest
            s = row[:pos] + '#' * blocks[blockind] + '.' + row[pos + blocks[blockind] + 1:]
            # does this position violate existing #:s?
            if s.count('#') > sum(blocks):
                continue
            if blockind < len(blocks) - 1:
                # more blocks to go, recurse!
                solutions += find_solutions(s, blocks, start=(pos + blocks[blockind] + 1), blockind=blockind+1)
            else:
                solutions.append(s.replace('?', '.'))
    return solutions

total = 0
with open('input.txt', 'r') as fp:
    for line in fp:
        row, numbers = re.match('([?.#]+) (.*)', line).groups()
        numbers = list(map(int, re.findall('([0-9]+)', numbers)))
        solns = find_solutions(row, numbers)
        total += len(solns)

assert total == 8419
