def get_operand(data, pos, mode):
    if mode == 0:
        return data[data[pos]]
    else:
        return data[pos]

def compute(data, max_iter=None):
    position = 0
    iter = 0
    last_output = None
    while True:
        iter += 1
        # first parse the instruction command and its parameter modes
        val = "00000" + str(data[position])
        cmd = int(val[-2:])
        # get three parameter modes
        pmodes = [int(val[n]) for n in (-3, -4, -5)]

        # now
        if cmd == 99:
            print("done")
            break
        if cmd == 1:
            operand1 = get_operand(data, position+1, pmodes[0])
            operand2 = get_operand(data, position+2, pmodes[1])
            data[data[position + 3]] = operand1 + operand2
            position += 4
        elif cmd == 2:
            operand1 = get_operand(data, position+1, pmodes[0])
            operand2 = get_operand(data, position+2, pmodes[1])
            data[data[position + 3]] = operand1 * operand2
            position += 4
        elif cmd == 3:
            print("****** input 1")
            data[data[position + 1]] = 1  # only input right now
            position += 2
        elif cmd == 4:
            val = get_operand(data, position+1, pmodes[0])
            print(f"****** output:", val)
            last_output = val
            position += 2
        else:
            raise ValueError(f"Unknown command at index {position}: {cmd}")

        if iter == max_iter:
            break
    return last_output

with open("input.txt", "r") as fp:
    data = list(map(int, fp.readline().split(",")))

assert compute(data) == 13933662
