import re
import numpy as np

# parse
with open('input.txt', 'r') as fp:
    for line in fp:
        data = re.findall('([0-9]+)', line)
        data = int(''.join(data))
        if re.match('.*Time:', line):
            time = data
        if re.match('.*Distance:', line):
            record = data

# calculate how far we'd get for each possible charging time
charging_time = np.arange(time + 1)
answer = ((time - charging_time) * charging_time > record).sum()

assert answer == 35349468
