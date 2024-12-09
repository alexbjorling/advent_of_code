with open("input.txt", "r") as fp:
    data = list(map(int, fp.read().strip()))

def parse(line):
    """
    Take the compact input list, and parse to file blocks, -1 means space.
    """
    ret = []
    fid = 0
    for i in range(len(line)):
        if i % 2 == 0:
            # file
            ret += [fid,] * line[i]
            fid += 1
        else:
            # gap
            ret += [-1,] * line[i]
    return ret

def compress(line):
    """
    Compress the list by the rules of the exercise.
    """
    out = line.copy()
    tot = len([x for x in line if x != -1])
    for n in line[::-1]:
        if n == -1:
            continue
        # see where to put it
        i2 = out.index(-1)
        if i2 > tot:
            break
        out[i2] = n
    return(out[:tot])

def check(line):
    """
    Sum up the compressed disk.
    """
    tot = 0
    for i, n in enumerate(line):
        tot += i * n
    return tot

assert check(compress(parse(data))) == 6288707484810