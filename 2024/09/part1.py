
with open("input.txt", "r") as fp:
    data = list(map(int, fp.read().strip()))

def expand(line):
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
    out = line.copy()
    import numpy as np
    tot = len(np.where(np.array(line) != -1)[0])
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
    tot = 0
    for i, n in enumerate(line):
        tot += i * n
    return tot

print(check(compress(expand(data))))