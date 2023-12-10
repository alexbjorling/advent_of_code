# load data and find the starting position
i, j = None, None
with open('input.txt', 'r') as fp:
    data = fp.read().strip().split('\n')
for ii in range(len(data)):
    if 'S' in data[ii]:
        i = ii
        j = data[ii].index('S')
assert None not in (i, j)

# look for a connection to start with
if (i > 0) and (data[i - 1][j] in '7F-'):
    direction = (-1, 0)
elif (i < len(data) - 1) and (data[i + 1][j] in 'JL-'):
    direction = (1, 0)
elif  (j > 0) and (data[i][j - 1] in 'FL|'):
    direction = (0, -1)
elif (j < len(data[0]) - 1) and (data[i][j + 1] in 'J7|'):
    direction = (0, 1)

def update_direction(old, pipe):
    """
    Helper to look up the new direction, given the way we came in and the pipe type
    """
    if pipe in '|-':
        return old
    elif pipe in 'JF':
        return (-old[1], -old[0])
    elif pipe in '7L':
        return old[::-1]
    elif pipe == 'S':
        return (0, 0)
    else:
        raise Exception('Should not get here')

# go around the loop
loop = []
while direction != (0, 0):
    loop.append((i, j))
    i += direction[0]
    j += direction[1]
    direction = update_direction(direction, data[i][j])

assert len(loop) // 2 == 6754
