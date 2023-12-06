import re


class Range(object):
	"""
	Trivial helper class to represent a continuous range of integers
	"""
	def __init__(self, start, num):
		self.start = start
		self.num = num
		self.max = start + num - 1

	def overlap(self, other):
		return (self.start <= other.max and self.max >= other.start)

	def split(self, pos):
		# split range so that pos becomes a new first element
		ret = [Range(self.start, pos - self.start), Range(pos, self.num - (pos - self.start))]
		assert ret[0].num > 0 and ret[1].num > 0, 'Couldn''t split range at %d' % pos
		return ret

	def partial_overlap(self, other):
		# return the first value at which our range should be split
		# to not overlap with <other>, or None if there's no overlap.
		if (self.start <= other.max) and (self.max > other.max):
			# our range crosses the upper bound of other
			return other.max + 1
		elif (self.max >= other.start) and (self.start < other.start):
			# our range crosses the lower bound of other
			return other.start
		else:
			return None

	def contains(self, num):
		return (num >= self.start) and (num <= self.max)

	def __str__(self):
		return '[%d, %d]' % (self.start, self.max)


class Map(object):
	"""
	Helper class which holds a map and can operate on lists of Range objects
	"""
	def __init__(self, lines=[]):
		self.lines = lines

	def map(self, r):
		# takes a single range and returns a list of mapped ranges
		###################################################################################################################################################
		####### problem here is that we return in the lines loop and so only treat the first line of each map     ##########################
		##################################################################################################################
		mapped_ranges = []  # a list of ranges that are done and shouldn't be operated on
		for line in self.lines:
			dest_start, src_start, range_length = line
			src_range = Range(src_start, range_length)
			intersection = r.partial_overlap(src_range)
			if intersection is None:
				if src_range.contains(r.start):
					# whole range is mapped
					return [Range(dest_start + (r.start - src_start), r.num)]
				else:
					# none of the range is mapped
					return [r,]
			else:
				ret = []
				for r_ in r.split(intersection):
					ret += self.map(r_)
				return ret

# text parsing - assuming maps are in order
seeds = []
maps = []
with open('ex.txt', 'r') as fp:
	for line in fp:
		if 'seeds:' in line:
			seeds_ = list(map(int, re.findall('([0-9]+)', line)))
			seeds = [Range(seeds_[i], seeds_[i+1]) for i in range(0, len(seeds_), 2)]
		elif 'map:' in line:
			maps.append(Map(lines=[]))
		else:
			numbers = list(map(int, re.findall('([0-9]+)', line)))
			if len(numbers):
				maps[-1].lines.append(numbers)

minima = []
for s in seeds:
	seeds_in = [s,]
	print('*** seed:', str(s))
	for m in maps:
		seeds_out = []
		for s_ in seeds_in:
			seeds_out += m.map(s_)
		print('step: ', [str(s_) for s_ in seeds_out])
		seeds_in = seeds_out
	minima.append(min([r.start for r in seeds_out]))

print('*** ', min(minima), ' ***')