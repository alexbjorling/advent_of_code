def fuel(x):
    res = x // 3 - 2
    if res < 1:
        return 0
    else:
        return res + fuel(res)

sum = 0
with open("input.txt", "r") as fp:
    for line in fp:
        sum += fuel(int(line))

print(sum)