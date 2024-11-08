def compute(data):
    position = 0
    while True:
        # first parse the instruction command and its parameter modes
        val = "00000" + str(data[position])
        cmd = int(val[-2:])
        m1, m2, m3 = [int(val[n]) for n in (-3, -4, -5)]

        print("command ", cmd)

        # now
        if cmd == 99:
            break
        if cmd in (1, 2):
            if m1 == 0:
                operand1 = data[data[position + 1]]
            else:
                operand1 = data[position + 1]
            if m2 == 0:
                operand2 = data[data[position + 2]]
            else:
                operand2 = data[position + 2]
            target = data[position + 3]
            print("parameter modes ", m1, m2)

        if cmd == 1:
            data[target] = operand1 + operand2
            position += 4
        elif cmd == 2:
            data[target] = operand1 * operand2
            position += 4
        elif cmd == 3:
            print("****** input")
            data[data[position + 1]] = 1  # only input right now
            position += 2
        elif cmd == 4:
            print("****** output: ", data[position + 1])
            position += 2
        else:
            raise ValueError(f"Unknown command at index {position}: {cmd}")
    return data[0]

with open("input.txt", "r") as fp:
    data = list(map(int, fp.readline().split(",")))

compute(data)