mn, mx = 353096, 843212

def is_non_decreasing(n):
    # is the digits of this number non-decreasing?
    s = str(n)
    for i in range(1, len(s)):
        if int(s[i]) < int(s[i-1]):
            return False
    return True

def has_strict_double(n):
    # does this number have a pair of identical adjacent numbers that's
    # not a part of a larger group of identical numbers?
    s = str(n)

    # make a list of the size of each group of identical numbers
    last = ''
    groups = []
    for i in range(len(s)):
        if s[i] == last:
            groups[-1] += 1
        else:
            groups.append(1)
        last = s[i]

    # see if any of them had size 2
    return (2 in groups)

cnt = 0
for i in range(mn, mx + 1):
    if is_non_decreasing(i) and has_strict_double(i):
        cnt += 1

assert cnt == 358
