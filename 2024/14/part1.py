import re

# load the data naively
robots = []
with open("input.txt", "r") as fp:
    for line in fp:
        numbers = list(map(int, re.findall("(\-?\d+)", line)))
        robots.append((numbers[:2], numbers[2:]))

shape = [101, 103]

# step the robots forward in one go, the % operator fixes the edges
for i, r in enumerate(robots):
    pos, vel = r
    pos = (
        (pos[0] + vel[0] * 100) % shape[0],
        (pos[1] + vel[1] * 100) % shape[1],
    )
    robots[i] = (pos, vel)

# count robots in quadrants of the board
q1, q2, q3, q4 = 0, 0, 0, 0
for r in robots:
    pos, vel = r
    if pos[0] < shape[0] // 2 and pos[1] < shape[1] // 2:
        q1 += 1
    elif pos[0] < shape[0] // 2 and pos[1] > shape[1] // 2:
        q2 += 1
    elif pos[0] > shape[0] // 2 and pos[1] > shape[1] // 2:
        q3 += 1
    elif pos[0] > shape[0] // 2 and pos[1] < shape[1] // 2:
        q4 += 1

assert q1 * q2 * q3 * q4 == 231782040
