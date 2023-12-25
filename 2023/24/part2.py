from sympy import solve, symbols

# First ideas were to parametrize each line, then for the first three
# lines find the time parameter which brought the points in line with
# each other. Those points should then be our stone's path. The system
# of equations was the dot products of the two vectors separating the
# three points. Didn't work with a numerical solution, not sure why!


class Stone:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel


stones = []
with open('input.txt', 'r') as fp:
    for line in fp:
        pos, vel = line.split('@')
        pos = list(map(int, pos.strip().split(',')))
        vel = list(map(int, vel.strip().split(',')))
        stones.append(Stone(pos, vel))

# 3 positions and velocities to solve for
p0x, p0y, p0z = symbols('p0x, p0y, p0z', integer=True)
vx, vy, vz = symbols('vx, vy, vz', integer=True)

# N times to solve for, so with N=3 we have 9 unknowns and 9 equations.
N = 3
times = symbols(','.join(['t%d'%n for n in range(N)]), integer=True, positive=True)

# Build and solve the system of equations
eqns = []
for i in range(N):
    t = times[i]
    sx_, sy_, sz_ = stones[i].pos
    vx_, vy_, vz_ = stones[i].vel
    eqns += [
        p0x + t * vx - (sx_ + t * vx_),
        p0y + t * vy - (sy_ + t * vy_),
        p0z + t * vz - (sz_ + t * vz_),
        ]
sol = solve(eqns, dict=True)
total = sum([sol[0][var] for var in (p0x,p0y,p0z)])

assert total == 549873212220117
