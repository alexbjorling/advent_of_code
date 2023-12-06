import re

# helper class for the mapping
class Map(object):
	def __init__(self, lines):
		self.lines = lines

	def map(self, number):
		mapped = None
		for line in self.lines:
			dest_start, src_start, range_length = line
			if (number >= src_start) and (number < src_start + range_length):
				mapped = dest_start + number - src_start
		return number if mapped is None else mapped

# text parsing - assuming maps are in order
seeds = []
maps = []
with open('input.txt', 'r') as fp:
	for line in fp:
		if 'seeds:' in line:
			seeds = list(map(int, re.findall('([0-9]+)', line)))
		elif 'map:' in line:
			maps.append(Map(lines=[]))
		else:
			numbers = list(map(int, re.findall('([0-9]+)', line)))
			if len(numbers):
				maps[-1].lines.append(numbers)

# now do the work
results = []
for s in seeds:
	num = s
	for m in maps:
		num = m.map(num)
	results.append(num)

assert min(results) == 227653707
