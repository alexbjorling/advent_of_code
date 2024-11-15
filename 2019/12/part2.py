import re
import numpy as np

# helper class
class Moon:
    def __init__(self, initstr):
        # construct from string like <x=10,y=-8,z=2>
        xyz = [int(re.findall(f".*{var}=(.?[\d]+).*", initstr)[0]) for var in "xyz"]
        self.pos = np.array(xyz)
        self.vel = np.zeros(3, dtype=int)

    def step(self):
        self.pos[:] += self.vel

    def energy(self):
        pot = np.sum(np.abs(self.pos))
        kin = np.sum(np.abs(self.vel))
        return pot * kin

    @property
    def state(self):
        return tuple(zip(tuple(self.pos), tuple(self.vel)))

# make some Moon objects
with open("input.txt", "r") as fp:
    moons = [Moon(line) for line in fp]

# looking for patterns...
xst0 = [(m.pos[0], m.vel[0]) for m in moons]
yst0 = [(m.pos[1], m.vel[1]) for m in moons]
zst0 = [(m.pos[2], m.vel[2]) for m in moons]

periods = [None, None, None]

n = 0
while None in periods:

    # update velocities pairwise
    for i in range(len(moons)):
        for j in range(i):
            signs = np.sign(moons[j].pos - moons[i].pos)
            moons[j].vel[:] -= signs
            moons[i].vel[:] += signs

    # update positions individually
    for m in moons:
        m.step()

    # number of updates done
    n += 1

    # are we back to the initial state?
    xst = [(m.pos[0], m.vel[0]) for m in moons]
    yst = [(m.pos[1], m.vel[1]) for m in moons]
    zst = [(m.pos[2], m.vel[2]) for m in moons]
    if xst == xst0:
        periods[0] = n
    if yst == yst0:
        periods[1] = n
    if zst == zst0:
        periods[2] = n


# demand getting back to initial states: 669891032576088, too high
assert np.lcm.reduce(periods) // 2 == 334945516288044  # don't understand the factor 2
