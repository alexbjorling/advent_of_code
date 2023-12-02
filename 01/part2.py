import re

words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
searchstr = '|'.join(words + ['\d'])

lookup = {w: str(n) for w, n in zip(words, range(10))}
lookup.update({str(i): str(i) for i in range(10)})

total = 0
with open('input.txt', 'r') as fp:
    for line in fp:
        # (?=...) matches but does not consume
        matches = re.findall('(?=(%s))' % searchstr, line)
        total += int(lookup[matches[0]] + lookup[matches[-1]])
print(total)
