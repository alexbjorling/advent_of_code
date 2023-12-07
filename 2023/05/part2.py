"""
Now ranges are represented by simple tuples (min, max), with min and max inclusive.
"""

import re

# helper class for the mapping
class Map(object):
    def __init__(self, lines):
        self.lines = lines

    def map_ranges(self, ranges):
        """
        Map a list of source ranges to a list of destination ranges
        """
        line_input = ranges
        mapped = []
        for line in self.lines:
            dest_start, src_start, range_length = line
            src_end = src_start + range_length - 1
            shift = dest_start - src_start
            remaining_input = []
            for r in line_input:
                if (r[1] < src_start) or (r[0] > src_end):  # this range is not mapped
                    remaining_input.append(r)
                elif (r[0] >= src_start) and (r[1] <= src_end):  # this whole range is mapped
                    mapped.append((r[0] + shift, r[1] + shift))
                elif (r[0] < src_start) and (r[1] >= src_start) and (r[1] <= src_end):  # top of this range is mapped but not bottom
                    remaining_input.append((r[0], src_start - 1))
                    overlap = r[1] - src_start + 1
                    mapped.append((dest_start, dest_start + overlap - 1))
                elif (r[0] >= src_start) and (r[0] <= src_end) and (r[1] > src_end):  # bottom of this range is mapped but not top
                    overshoot = r[1] - src_end
                    mapped.append((r[0] + shift, src_end + shift))
                    remaining_input.append((src_end + 1, src_end + overshoot))
                elif (r[0] < src_start) and (r[1] > src_end):  # middle of this range is mapped but not ends
                    before = src_start - r[0]
                    after = r[1] - src_end
                    mapped.append((dest_start, dest_start + range_length - 1))
                    remaining_input.append((src_start - before, src_start - 1))
                    remaining_input.append((src_end + 1, src_end + after))
                else:
                    raise Exception('Should not get here (%s, (%d,%d))!' % (r, src_start, src_end))
            line_input = remaining_input
        return remaining_input + mapped

# text parsing - assuming maps are in order
seeds = []
maps = []
with open('input.txt', 'r') as fp:
    for line in fp:
        if 'seeds:' in line:
            seeds_ = list(map(int, re.findall('([0-9]+)', line)))
            seeds = [(seeds_[i], seeds_[i] + seeds_[i+1] - 1) for i in range(0, len(seeds_), 2)]
        elif 'map:' in line:
            maps.append(Map(lines=[]))
        else:
            numbers = list(map(int, re.findall('([0-9]+)', line)))
            if len(numbers):
                maps[-1].lines.append(numbers)

for m in maps:
    seeds = m.map_ranges(seeds)

result = min([r[0] for r in seeds])
assert result == 78775051
