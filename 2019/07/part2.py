from itertools import permutations

class Intcode:
    def __init__(self, program):
        self.prog = program.copy()
        self.halted = False
        self.pos = 0
        self.n_runs = 0
        self.last_output = None

    def get_operand(self, pos, mode):
        if mode == 0:
            return self.prog[self.prog[pos]]
        else:
            return self.prog[pos]

    def run(self, inputs=None, return_on_output=False):
        self.n_runs += 1
        while True:
            # first parse the instruction command and its parameter modes
            val = "00000" + str(self.prog[self.pos])
            cmd = int(val[-2:])
            # get three parameter modes
            pmodes = [int(val[n]) for n in (-3, -4, -5)]

            # now
            if cmd == 99:
                self.halted = True
                print("done")
                return None
            if cmd == 1:
                operand1 = self.get_operand(self.pos+1, pmodes[0])
                operand2 = self.get_operand(self.pos+2, pmodes[1])
                self.prog[self.prog[self.pos + 3]] = operand1 + operand2
                self.pos += 4
            elif cmd == 2:
                operand1 = self.get_operand(self.pos+1, pmodes[0])
                operand2 = self.get_operand(self.pos+2, pmodes[1])
                self.prog[self.prog[self.pos + 3]] = operand1 * operand2
                self.pos += 4
            elif cmd == 3:
                inpt = inputs.pop(0)
                self.prog[self.prog[self.pos + 1]] = inpt
                self.pos += 2
            elif cmd == 4:  # output
                val = self.get_operand(self.pos+1, pmodes[0])
                self.last_output = val
                print("*** output:", val)
                self.pos += 2
                if return_on_output:
                    return val
            elif cmd == 5:  # jump-if-true
                cond = self.get_operand(self.pos+1, pmodes[0])
                dest = self.get_operand(self.pos+2, pmodes[1])
                if cond != 0:
                    self.pos = dest
                else:
                    self.pos += 3
            elif cmd == 6:  # jump-if-false
                cond = self.get_operand(self.pos+1, pmodes[0])
                dest = self.get_operand(self.pos+2, pmodes[1])
                if cond == 0:
                    self.pos = dest
                else:
                    self.pos += 3
            elif cmd == 7:  # less-than
                operand1 = self.get_operand(self.pos+1, pmodes[0])
                operand2 = self.get_operand(self.pos+2, pmodes[1])
                result = int(operand1 < operand2)
                self.prog[self.prog[self.pos + 3]] = result
                self.pos += 4
            elif cmd == 8:  # equals
                operand1 = self.get_operand(self.pos+1, pmodes[0])
                operand2 = self.get_operand(self.pos+2, pmodes[1])
                result = int(operand1 == operand2)
                self.prog[self.prog[self.pos + 3]] = result
                self.pos += 4
            else:
                raise ValueError(f"Unknown command at index {self.pos}: {cmd}")


with open("input.txt", "r") as fp:
    data = list(map(int, fp.readline().split(",")))

totals = []
for phases in permutations(range(5, 10)):
    computers = [Intcode(data) for i in range(5)]
    last_output = 0
    done = False
    while not done:
        for i in range(len(computers)):
            # first time, give both the phase setting and the first input
            inpt = [phases[i], last_output] if computers[i].n_runs==0 else [last_output,]
            last_output = computers[i].run(inpt, return_on_output=True)
            if computers[i].halted:
                print("computer", i, "halted")
                done = True
    totals.append(computers[-1].last_output)

assert max(totals) == 4275738