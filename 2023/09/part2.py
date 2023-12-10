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

	# do the expansion with negative coefficients for odd derivatives (it's a Tayor expansion)
	derivatives_ = np.array([d[0] for d in derivatives])
	signs = (-1) ** np.arange(len(derivatives))
	total += sum(signs * derivatives_)

assert total == 1077
