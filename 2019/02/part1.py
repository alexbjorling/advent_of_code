with open("input.txt", "r") as fp:
    data = list(map(int, fp.readline().split(",")))

data[1] = 12
data[2] = 2

position = 0
while True:
    cmd = data[position]
    if cmd == 99:
        break
    operands = data[data[position+1]], data[data[position+2]]
    target = data[position+3]
    if cmd == 1:
        data[target] = operands[0] + operands[1]
    elif cmd == 2:
        data[target] = operands[0] * operands[1]
    else:
        raise ValueError(f"Unknown command at index {position}: {cmd}")
    position += 4

assert data[0] == 4945026
