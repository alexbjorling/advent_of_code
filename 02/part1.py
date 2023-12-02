import re

cube_max = {'red': 12, 'green': 13, 'blue': 14}

with open('input.txt', 'r') as fp:
	total = 0
	for line in fp:
		game_id = int(re.findall('Game (\d+)', line)[0])
		# tried to do this with only regex, but just couldn't - so splitting on ':' and ':' first
		sets = line.split(':')[1].split(';')
		ok = True
		for s in sets:
			cubes = re.findall('(\d+) (green|blue|red)', s)
			cubes = {col: int(num) for num, col in cubes}
			for col, num in cubes.items():
				if num > cube_max[col]:
					ok = False
		if ok:
			total += game_id

print(total)