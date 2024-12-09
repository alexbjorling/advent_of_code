
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

def expand(line):
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
    N = len([f for f in inp if isinstance(f, File)])
    out = inp.copy()
    for i1 in range(1, len(inp)):
        f1 = inp[-i1]
        if isinstance(f1, Space):
            continue
        for i2 in range(len(out)):
            f2 = out[i2]
            if isinstance(f2, Space) and f2.width >= f1.width:
                out[i2] = f1
                diff = f2.width - f1.width
                if diff > 0:
                    if isinstance(out[i2 + 1], Space):
                        print('y')
                        out[i2 + 1] = Space(diff + out[i2 + 1].width)
                    else:
                        print('n')
                        out.insert(i2 + 1, Space(diff))
                break
    return out

def check(line):
    tot = 0
    for i, n in enumerate(line):
        if n == -1:
            continue
        tot += i * n
    return tot

def expand2(line):
    out = []
    done = set()
    print([str(c) for c in line])
    for f in line:
        if isinstance(f, File) and f.id not in done:
            out += [f.id,] * f.width
            done.add(f.id)
        else:
            out += [0,] * f.width
    print([c for c in out])
    return out

print(check(expand2(compress(expand(data)))))
