import numpy as np
import re

# load data
sequences = []
with open('input.txt', 'r') as fp:
	for line in fp:
		sequences.append(list(map(int, re.findall('(-?[0-9]+)', line))))

total = 0
for seq in sequences:

	# do the derivatives
	derivatives = [seq]
	while not (np.all(derivatives[-1] == 0)):
		derivatives.append(np.diff(derivatives[-1]))

	# do the expansion
	total += sum(([d[-1] for d in derivatives]))

total == 2005352194