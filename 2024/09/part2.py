
with open("input.txt", "r") as fp:
    data = list(map(int, fp.read().strip()))


class Space():
    def __init__(self, width):
        self.width = width
    def __str__(self):
        return ' ' * self.width

class File():
    def __init__(self, width, id):
        self.width = width
        self.id = id
    def __str__(self):
        return str(self.id) * self.width

def parse(line):
    """
    Parse the input into a list of Space and File objects
    """
    ret = []
    fid = 0
    for i in range(len(line)):
        if i % 2 == 0:
            # file
            ret.append(File(width=line[i], id=fid))
            fid += 1
        else:
            # gap
            ret.append(Space(width=line[i]))
    return ret

def compress(inp):
    """
    Compress the list of Space and File objects by the rules of the exercise.
    """
    N = len([f for f in inp if isinstance(f, File)])
    out = inp.copy()

    # loop over all files, starting on the right
    for f1 in inp[::-1]:
        if not isinstance(f1, File):
            continue

        # for the current state of the output list, where is f1?
        i1 = [(isinstance(f_, File) and f_.id==f1.id) for f_ in out].index(True)

        # is there space anywhere on the left?
        for i2 in range(i1):
            f2 = out[i2]
            if isinstance(f2, Space) and f2.width >= f1.width:
                # good, now replace f1 with space, and put f1 where the space was
                out[i2] = f1
                out[i1] = Space(f1.width)
                # see if we should add more space to the right of f1, either by inserting
                # a new Space or by increasing the size of one already there.
                diff = f2.width - f1.width
                if diff > 0:
                    if isinstance(out[i2 + 1], Space):  # never actually used, but could have been important
                        out[i2 + 1] = Space(out[i2 + 1].width + diff)
                    else:
                        out.insert(i2 + 1, Space(diff))
                break
    return out

def expand(line):
    """
    Expand the files and spaces to a list of blocks, each with the id of its file (spaces are 0).
    """
    out = []
    done = set()
    for f in line:
        if isinstance(f, File) and f.id not in done:
            out += [f.id,] * f.width
            done.add(f.id)
        else:
            out += [0,] * f.width
    return out

def check(line):
    """
    Sum up the compressed disk
    """
    tot = 0
    for i, n in enumerate(line):
        if n == -1:
            continue
        tot += i * n
    return tot



assert check(expand(compress(parse(data)))) == 6311837662089