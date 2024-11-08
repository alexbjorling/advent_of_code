mn, mx = 353096, 843212

def is_non_decreasing(n):
    # is the digits of this number non-decreasing?
    s = str(n)
    for i in range(1, len(s)):
        if int(s[i]) < int(s[i-1]):
            return False
    return True

def has_double(n):
    # does this number have a pair of identical adjacent numbers?
    s = str(n)
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            return True
    return False

cnt = 0
for i in range(mn, mx + 1):
    if is_non_decreasing(i) and has_double(i):
        cnt += 1

assert cnt == 579