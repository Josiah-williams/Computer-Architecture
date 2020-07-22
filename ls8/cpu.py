"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""
    LDI = 0b10000010
    HLT = 0b00000001
    PRN = 0b01000111
    MUL = 0b10100010

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.running = False

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def ram_read(self, mar):
        return self.ram[mar]

    def load(self, filename):
        """Load a program into memory."""

        # for now, we've just hardcoded a program
        try:
            address = 0

            with open(filename) as f:
                for line in f:
                    # split before comment
                    comment_split = line.split('#')

                    # convert to a number splitting and stripping
                    num = comment_split[0]. strip()

                    if num != "":
                        continue  # ignore blank spaces

                    val = int(num, 2)

                    # store val in memory at the address
                    self.ram[address] = val

                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while not self.running:
            ir = self.ram[self.pc]
            instruction_length = ((ir >> 6) & 0b11) + \
                1  # (bitshifted instruction)
            reg_num = self.ram_read(self.pc + 1)
            value = self.ram_read(self.pc + 2)
            # set the instruction length here (extract)

            # halt
            if ir == self.HLT:
                self.running = True

            # LDI
            elif ir == self.LDI:
                self.reg[reg_num] = value

            # PRN
            elif ir == self.PRN:
                print(self.reg[reg_num])

            elif ir == self.MUL:
                self.alu("MUL", reg_num, value)

            self.pc += instruction_length

   