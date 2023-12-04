import re

total = 0
with open('input.txt', 'r') as fp:
    for line in fp:
        # trying hard to do all-regex parsing - no split or strip!
        row = re.match('(?:Card\s+[0-9]+):(.*)', line).groups()[0]
        winners, numbers = re.match('(.*)\|(.*)', row).groups()
        winners = list(map(int, re.findall('([0-9]+)', winners)))
        numbers = list(map(int, re.findall('([0-9]+)', numbers)))

        # now check and sum up
        matches = sum([(n in winners) for n in numbers])
        total += int(2**(matches - 1))  # int(2**(-1)) = 0

assert total == 23847
print(total)
