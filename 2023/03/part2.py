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
	# get Match objects for all asterisks on this line and loop over them
	for asterisk in re.finditer('(\*)', lines[i]):
		pos = asterisk.span()[0]
		# now find all the numbers on this and the adjacent lines which neighbor the asterisk
		numbers = []
		for line in lines[i-1:i+2]:
			for number in re.finditer('([0-9]+)', line):
				if (number.span()[0] <= pos + 1) and (number.span()[1] >= pos):
					numbers.append(int(number.groups()[0]))
		# and include if there are two such numbers
		if len(numbers) == 2:
			total += numbers[0] * numbers[1]

print(total)
