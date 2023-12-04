import re
import numpy as np

with open('input.txt', 'r') as fp:
	total = 0
	for line in fp:
		game_id = int(re.findall('Game (\d+)', line)[0])
		# tried to do this with only regex, but just couldn't - so splitting on ':' and ':' first
		sets = line.split(':')[1].split(';')
		cube_min = {'red': 0, 'green': 0, 'blue': 0}
		for s in sets:
			cubes = re.findall('(\d+) (green|blue|red)', s)
			cubes = {col: int(num) for num, col in cubes}
			for col, num in cubes.items():
				cube_min[col] = max(cube_min[col], num)
		total += np.prod(list(cube_min.values()))

print(total)
