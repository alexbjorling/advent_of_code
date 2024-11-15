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

# make some Moon objects
with open("input.txt", "r") as fp:
    moons = [Moon(line) for line in fp]

for n in range(1000):
    # update velocities pairwise
    for i in range(len(moons)):
        for j in range(i):
            signs = np.sign(moons[j].pos - moons[i].pos)
            moons[j].vel[:] -= signs
            moons[i].vel[:] += signs

    # update positions individually
    for m in moons:
        m.step()

energy = np.sum([m.energy() for m in moons])
assert energy == 7687
