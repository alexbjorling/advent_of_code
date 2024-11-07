def compute(data):
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
    return data[0]


for noun in range(100):
    for verb in range(100):
        with open("input.txt", "r") as fp:
            data = list(map(int, fp.readline().split(",")))

        data[1] = noun
        data[2] = verb

        if compute(data) == 19690720:
            answers = noun, verb

assert 100 * answers[0] + answers[1] == 5296
