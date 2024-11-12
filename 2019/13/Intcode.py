class Intcode:
    def __init__(self, program):
        self.prog = program.copy()
        self.halted = False
        self.pos = 0
        self.n_runs = 0
        self.relative_base = 0
        self.inputs = []

    def get_value(self, addr):
        self.ensure_addr(addr)
        return self.prog[addr]

    def set_value(self, addr, val):
        self.ensure_addr(addr)
        self.prog[addr] = val

    def ensure_addr(self, addr):
        # extend the program's memory if needed
        if addr > len(self.prog) - 1:
            missing = addr - len(self.prog) + 1
            self.prog.extend([0, ] * missing)

    def read_by_mode(self, pos, mode):
        # find the absolute address to read from
        if mode == 0:
            addr = self.get_value(pos)
        elif mode == 1:
            addr = pos
        elif mode == 2:
            addr = self.get_value(pos) + self.relative_base

        return self.get_value(addr)

    def write_by_mode(self, pos, mode, val):
        if mode == 0:
            addr = self.get_value(pos)
        elif mode == 2:
            addr = self.get_value(pos) + self.relative_base

        self.set_value(addr, val)

    def run(self):
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
            if cmd == 1:  # addition
                operand1 = self.read_by_mode(self.pos+1, pmodes[0])
                operand2 = self.read_by_mode(self.pos+2, pmodes[1])
                self.write_by_mode(self.pos+3, pmodes[2], operand1 + operand2)
                self.pos += 4
            elif cmd == 2:  # multiplication
                operand1 = self.read_by_mode(self.pos+1, pmodes[0])
                operand2 = self.read_by_mode(self.pos+2, pmodes[1])
                self.write_by_mode(self.pos+3, pmodes[2], operand1 * operand2)
                self.pos += 4
            elif cmd == 3:  # input
                if self.inputs is None or len(self.inputs) == 0:
                    return None  # have to call again with the input
                inpt = self.inputs.pop(0)
                self.write_by_mode(self.pos+1, pmodes[0], inpt)
                self.pos += 2
            elif cmd == 4:  # output
                val = self.read_by_mode(self.pos+1, pmodes[0])
                self.last_output = val
                self.pos += 2
                return val
            elif cmd == 5:  # jump-if-true
                cond = self.read_by_mode(self.pos+1, pmodes[0])
                dest = self.read_by_mode(self.pos+2, pmodes[1])
                if cond != 0:
                    self.pos = dest
                else:
                    self.pos += 3
            elif cmd == 6:  # jump-if-false
                cond = self.read_by_mode(self.pos+1, pmodes[0])
                dest = self.read_by_mode(self.pos+2, pmodes[1])
                if cond == 0:
                    self.pos = dest
                else:
                    self.pos += 3
            elif cmd == 7:  # less-than
                operand1 = self.read_by_mode(self.pos+1, pmodes[0])
                operand2 = self.read_by_mode(self.pos+2, pmodes[1])
                result = int(operand1 < operand2)
                self.write_by_mode(self.pos+3, pmodes[2], result)
                self.pos += 4
            elif cmd == 8:  # equals
                operand1 = self.read_by_mode(self.pos+1, pmodes[0])
                operand2 = self.read_by_mode(self.pos+2, pmodes[1])
                result = int(operand1 == operand2)
                self.write_by_mode(self.pos+3, pmodes[2], result)
                self.pos += 4
            elif cmd == 9:  # adjust relative base
                shift = self.read_by_mode(self.pos+1, pmodes[0])
                self.relative_base += shift
                self.pos += 2
            else:
                raise ValueError(f"Unknown command at index {self.pos}: {cmd}")