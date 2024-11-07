sum = 0

with open("input.txt", "r") as fp:
    for line in fp:
        sum += int(line) // 3 - 2

print(sum)