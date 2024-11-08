from itertools import permutations

class Intcode:
    def __init__(self, program):
        self.prog = program.copy()

    def get_operand(self, pos, mode):
        if mode == 0:
            return self.prog[self.prog[pos]]
        else:
            return self.prog[pos]

    def run(self, inputs=None):
        position = 0
        last_output = None
        while True:
            # first parse the instruction command and its parameter modes
            val = "00000" + str(self.prog[position])
            cmd = int(val[-2:])
            # get three parameter modes
            pmodes = [int(val[n]) for n in (-3, -4, -5)]

            # now
            if cmd == 99:
                print("done")
                break
            if cmd == 1:
                operand1 = self.get_operand(position+1, pmodes[0])
                operand2 = self.get_operand(position+2, pmodes[1])
                self.prog[self.prog[position + 3]] = operand1 + operand2
                position += 4
            elif cmd == 2:
                operand1 = self.get_operand(position+1, pmodes[0])
                operand2 = self.get_operand(position+2, pmodes[1])
                self.prog[self.prog[position + 3]] = operand1 * operand2
                position += 4
            elif cmd == 3:
                inpt = inputs.pop(0)
                print("****** input", inpt)
                self.prog[self.prog[position + 1]] = inpt
                position += 2
            elif cmd == 4:
                val = self.get_operand(position+1, pmodes[0])
                print(f"****** output:", val)
                last_output = val
                position += 2
            elif cmd == 5:  # jump-if-true
                cond = self.get_operand(position+1, pmodes[0])
                dest = self.get_operand(position+2, pmodes[1])
                if cond != 0:
                    position = dest
                else:
                    position += 3
            elif cmd == 6:  # jump-if-false
                cond = self.get_operand(position+1, pmodes[0])
                dest = self.get_operand(position+2, pmodes[1])
                if cond == 0:
                    position = dest
                else:
                    position += 3
            elif cmd == 7:  # less-than
                operand1 = self.get_operand(position+1, pmodes[0])
                operand2 = self.get_operand(position+2, pmodes[1])
                result = int(operand1 < operand2)
                self.prog[self.prog[position + 3]] = result
                position += 4
            elif cmd == 8:  # equals
                operand1 = self.get_operand(position+1, pmodes[0])
                operand2 = self.get_operand(position+2, pmodes[1])
                result = int(operand1 == operand2)
                self.prog[self.prog[position + 3]] = result
                position += 4
            else:
                raise ValueError(f"Unknown command at index {position}: {cmd}")

        return last_output

with open("input.txt", "r") as fp:
    data = list(map(int, fp.readline().split(",")))

totals = []
for phases in permutations(range(5)):
    last_output = 0
    for i in range(5):
        computer = Intcode(data)
        last_output = computer.run([phases[i], last_output])
    totals.append(last_output)

assert max(totals) == 95757
