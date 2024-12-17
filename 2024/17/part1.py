import re

# load the data as an array of ascii values
with open("input.txt", "r") as fp:
    regs, prog = fp.read().split("\n\n")
    a, b, c = list(map(int, re.findall("(\d+)", regs)))
    program = list(map(int, re.findall("(\d+)", prog)))

def run(program, a, b, c):

    def get_val(operand):
        if operand < 4:
            return operand
        else:
            return {4: a, 5: b, 6: c}[operand]

    pointer = 0
    output = []
    while pointer < len(program):
        instr = program[pointer]
        operand = program[pointer + 1]
        combo = get_val(operand)

        if instr == 0:  # adv
            a = a // (2**combo)
        elif instr == 1:  # bxl
            b = b ^ operand  # bitwise xor
        elif instr == 2:  # bst
            b = combo % 8
        elif instr == 3:  # jnz
            if a != 0:
                pointer = operand
                continue
        elif instr == 4:  # bxc
            b = b ^ c
        elif instr == 5:  # out
            val = combo % 8
            output.append(val)
        elif instr == 6:  # bdv
            b = a // (2**combo)
        elif instr == 7:  # cdv
            c = a // (2**combo)

        pointer += 2

    return(output)

out = run(program, a, b, c)
assert ",".join(map(str, out)) == "6,7,5,2,1,3,5,1,7"