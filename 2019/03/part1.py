with open("input.txt", "r") as fp:
    w1 = fp.readline().strip().split(",")
    w2 = fp.readline().strip().split(",")

def render_corners(path):
    coords = [(0, 0)]
    for step in path:
        directions = {
            "L": (0, -1),
            "R": (0, 1),
            "U": (-1, 0),
            "D": (1, 0),
        }
        direction = directions[step[0]]
        n = int(step[1:])
        coords.append((
            coords[-1][0] + direction[0] * n,
            coords[-1][1] + direction[1] * n
        ))
    return coords

c1 = render_corners(w1)
c2 = render_corners(w2)

def parallel(l1, l2):
    # are two lines ((i1, j1), (i2, j2)) and ((i3, j3), (i4, j4)) parallel or not?
    (i1, j1), (i2, j2) = l1
    (i3, j3), (i4, j4) = l2
    both_horizontal = (i1 == i2 and i3 == i4)
    both_vertical = (j1 == j2 and j3 == j4)
    if both_vertical or both_horizontal:
        return True
    else:
        return False

def cross(l1, l2):
    # where do two lines ((i1, j1), (i2, j2)) and ((i3, j3), (i4, j4)) cross? None if they don't.
    if parallel(l1, l2):
        return None

    (i1, j1), (i2, j2) = l1
    (i3, j3), (i4, j4) = l2
    if j1 == j2:
        v = l1
        h = l2
    else:
        v = l2
        h = l1

    horizontal_overlap = min(h[0][1], h[1][1]) < v[1][1] and max(h[0][1], h[1][1]) > v[1][1]
    vertical_overlap = min(v[0][0], v[1][0]) < h[0][0] and max(v[0][0], v[1][0]) > h[0][0]
    if vertical_overlap and horizontal_overlap:
        return (h[0][0], v[0][1])


crossings = []
for i in range(1, len(c1)):
    for j in range(1, len(c2)):
        line1 = (c1[i], c1[i-1])
        line2 = (c2[j], c2[j-1])
        c = cross(line1, line2)
        if c is not None:
            crossings.append(c)

distances = [abs(c[0]) + abs(c[1]) for c in crossings[1:]]
assert min(distances) == 896
