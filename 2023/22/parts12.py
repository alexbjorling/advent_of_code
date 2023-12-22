import re
import copy
import numpy as np


class Brick:

    n_instances = 0

    def __init__(self, p1, p2):
        self.name = 'B' + str(Brick.n_instances + 1)
        Brick.n_instances += 1
        p1 = np.array(p1)
        p2 = np.array(p2)
        self.p1 = p1
        self.p2 = p2
        self.n = int(np.linalg.norm(p1 - p2) + 1)
        if self.n > 1:
            dp = (p2 - p1) / (self.n - 1)
        else:
            dp = 1
        self.blocks = [p1 + i * dp for i in range(self.n)]
        self.above = []
        self.below = []

    def zmax(self):
        # return the highest z plane of this brick
        return max(self.p1[2], self.p2[2]) + 1

    def zmin(self):
        # return the lowest z plane of this brick
        return min(self.p1[2], self.p2[2])

    def intersects_xy(self, other):
        # determine whether to bricks intersect when projected on the xy plane
        for i in range(self.n):
            for j in range(other.n):
                if np.all(self.blocks[i][:2] == other.blocks[j][:2]):
                    return True
        return False

    def supported_by(self, other):
        return (other.name in self.below) and (self.zmin() == other.zmax())

    def on_ground(self):
        return self.zmin() == 0

    def step_down(self, N=1):
        self.p1[2] -= N
        self.p2[2] -= N

    def __lt__(self, other):
        return self.zmin() < other.zmin()

    def __str__(self):
        return f'<{self.name}>'

bricks = []
with open('input.txt', 'r') as fp:
    for line in fp:
        numbers = list(map(int, re.match('(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)', line.strip()).groups()))
        bricks.append(Brick(numbers[:3], numbers[3:]))
bricks = {b.name: b for b in bricks}

# Once and for all figure out for each block which others it has
# above and below, bite the N**2 bullet here.
# O(N**2)
print('Doing O(2) work...')
for i in range(len(bricks)):
    percent = 100 * ((i + 1)**2 - 1) / 2 / (((len(bricks) + 1)**2 - 1) / 2)
    print(f'{int(percent)}%', end='\r', flush=True)
    for j in range(i):
        b1, b2 = list(bricks.values())[i], list(bricks.values())[j]
        if b1.intersects_xy(b2):
            if b1.zmin() > b2.zmin():
                b1.below.append(b2.name)
                b2.above.append(b1.name)
            else:
                b2.below.append(b1.name)
                b1.above.append(b2.name)

# Iteratively move the bricks down
# O(N)
print('Settling stack...')
settled = False
while not settled:
    settled = True
    for brick in sorted(bricks.values()):
        if brick.on_ground():
            continue
        free_distance = min([brick.zmin() - bricks[name].zmax() for name in brick.below] + [brick.zmin()])
        if free_distance:
            brick.step_down(free_distance)
            settled = False

# Part 1: check which can be disintegrated - those that have nothing sitting on them which isn't resting on something else
# O(N)
total = 0
for brick in bricks.values():
    supported_bricks = [bricks[name] for name in brick.above if bricks[name].supported_by(brick)]
    critical = False
    for s in supported_bricks:
        other_supports = [bricks[name] for name in s.below if s.supported_by(bricks[name]) and name!=brick.name]
        if not other_supports:
            critical = True
    if not critical:
        total += 1

#assert total == 509
print('part 1 OK')

# Part 2: tried recursion but it was too hard to count everything and double-count nothing
# Here we copy the whole set of bricks, remove one and let the others fall, counting
# how many bricks move.
print('Checking the effects of disintegrating each brick...')
total = 0
for brick in bricks.values():
    print(f'{brick.name}: {total}', end='\r')
    # copy and remove the current brick (including references)
    bricks_copy = copy.deepcopy(bricks)
    removed = bricks_copy.pop(brick.name)
    for b in removed.above:
        bricks_copy[b].below.remove(brick.name)
    for b in removed.below:
        bricks_copy[b].above.remove(brick.name)
    # now settle the rest of the stack
    settled = False
    moved = {}
    while not settled:
        settled = True
        for brick in sorted(bricks_copy.values()):
            if brick.on_ground():
                continue
            free_distance = min([brick.zmin() - bricks_copy[name].zmax() for name in brick.below] + [brick.zmin()])
            if free_distance:
                brick.step_down(free_distance)
                moved[brick.name] = 1
                settled = False
    total += sum(moved.values())
print('')

#assert total == 102770
print('part 2 OK')
