import re

# read everything into a big string
with open('input.txt', 'r') as fp:
	lines = fp.read().split('\n')

# pad with dots to make boundary cases easier later
empty = '.' * len(lines[0])
lines.insert(0, empty)
lines.append(empty)
lines = ['.' + line + '.' for line in lines]

# loop over all the lines and sum up
total = 0
for i in range(1, len(lines)-1):
	# get Match objects for all numbers on this line and loop over them
	matches = re.finditer('([0-9]+)', lines[i])
	for match in matches:
		# cut out the number's surrounding and search for symbols
		searchbox = ''
		for j in (-1, 0, 1):
			searchbox += lines[i + j][match.span()[0]-1:match.span()[1]+1]
		if re.search('[^0-9|^.]', searchbox):
			total += int(match.groups()[0])

print(total)
