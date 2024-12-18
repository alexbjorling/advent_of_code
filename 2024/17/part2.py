import re

# load the data as an array of ascii values
with open("input.txt", "r") as fp:
    regs, prog = fp.read().split("\n\n")
    program = list(map(int, re.findall("(\d+)", prog)))


# re-write the program as the binary operations it performs
def run(a):
    out = []
    while True:
        b = a % 8
        b = b ^ 3
        c = a >> b
        b = b ^ 5
        a = a >> 3
        b = b ^ c
        out.append(b % 8)
        if a == 0: break
    return out

# Observations:
# * only the last 10 bits of the input a affect the output, could start from there
# * a is right-shifted by 3 after each output, so the last number is produced by
#   just 3 bits, the second last by 6 bits, etc, and it might be easiest (Calle's
#   idea) to work backwards.

# Search backwards, first find the 3 bits that give the last program
# value, then find the next 3 bits, etc. We need to search the whole
# tree since the solutions for each 3-bit addition are not unique.
def search(a=0, depth=16):

    # are we done?
    if depth == 0:
        return [a,]

    # search all triplets which will give the right output at this depth,
    # then recurse for each
    options = []
    for triplet in range(8):
        a_new = (a << 3) + triplet
        res = run(a_new)
        if res == program[len(program) - len(res):]:
            options += search(a_new, depth-1)
    return options

assert(min(search())) == 216549846240877
