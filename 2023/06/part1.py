import re
import numpy as np

# parse
with open('input.txt', 'r') as fp:
    records, distances = [], []
    for line in fp:
        data = list(map(int, re.findall('([0-9]+)', line)))
        if re.match('.*Time:', line):
            records = data
        if re.match('.*Distance:', line):
            distances = data

# calculate how far we'd get for each possible charging time
total_ways = []
for t, d in zip(records, distances):
    charging_time = np.arange(t + 1)
    distance = (t - charging_time) * charging_time
    total_ways.append((distance > d).sum())

assert np.prod(total_ways) == 1710720
