"""CPU functionality."""

import sys


# opcodes
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
ADD = 0b10100000
RET = 0b00010001
SUB = 0b10100001
CMP = 0b10100111
# JMP = 0b01010100
# JEQ = 0b01010101
# JNE = 0b01010110


SP = 7

# Flags
LT = 0b00000100
GT = 0b00000010
EQ = 0b00000001



class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.halted = False
        self.flag_reg = [0] * 8
        self.bt = {
            HLT : self.HLT,
            PRN : self.PRN,
            LDI : self.LDI,
            MUL : self.MUL,
            ADD : self.ADD,
            SUB : self.SUB,
            PUSH : self.PUSH,
            POP : self.POP,
            CALL : self.CALL,
            RET : self.RET,
            CMP : self.CMP
        }

    def op_ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
    
    def op_prn(self, operand_a, operand_b):
        print(self.reg[operand_a])
    
    def op_hlt(self, operand_a, operand_b):
        sys.exit(0)
    
    def op_add(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)
    
    def op_mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
    
    def op_pop(self, operand_a, operand_b):
        self.reg[operand_a] = self.pop_val()
    
    def op_push(self, operand_a, operand_b):
        self.push_val(self.reg[operand_a])

    def op_call(self, operand_a, operand_b):
        # Pushing next instruction to stack
        self.push_val(self.pc + 2)
        # setting pc address of subroutine
        self.pc = self.reg[operand_a]

    def op_cmp(self, operand_a, operand_b):
        self.alu("CMP", operand_a, operand_b)

    def op_jmp(self, operand_a, operand_b):
        # Set the PC to the address stored in the given register
        self.pc = self.reg[operand_a]

    def op_jeq(self, operand_a, operand_b):
        # If equal flag is set (true), jump to the address stored in the given register
        if self.fl == EQ:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    def op_jne(self, operand_a, operand_b):
        # If E flag is clear (false, 0), jump to the address stored in the given register
        if not self.fl == EQ:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    def op_ret(self, operand_a, operand_b):
        # Poping next instruction off top of stack
        self.pc = self.pop_val()
    
    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr
    
    def ram_read(self, mar):
        return self.ram[mar]

    def load(self, filename):
        """Load a program into memory."""

        # For now, we've just hardcoded a program:
        try:
            address = 0

            with open(filename) as f:
                for line in f:
                    # split before comment
                    comment_split = line.split('#')

                    # convert to a number splitting and stripping
                    num = comment_split[0].strip()

                    if num == '':
                        continue  # ignore blank lines
                    
                    val = int(num, 2)
                    
                    # store val in memory at the given address
                    self.ram[address] = val

                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found!")
            sys.exit(2)

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "DIV":
            self.reg[reg_a] //= self.reg[reg_b]

        elif op == "CMP":
            # if they are equal
            if reg_a == reg_b:
            # set Equal E flag to 1 
                self.flag_reg[EQ] = 0b00000001
            # otherwise set to 0
            else:
                self.flag_reg[EQ] = 0b00000000
        else:
            raise Exception("unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while not self.halted:
            ir = self.ram[self.pc]
            instruction_length = ((ir >> 6) & 0b11) + 1 # (bitshifted instruction)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # set the instruction length here (extract)

            # halt
            if ir == HLT:
                self.halted = True
            
            # LDI
            elif ir == LDI:
                self.reg[operand_a] = operand_b

            # PRN
            elif ir == PRN:
                print(self.reg[operand_a])

            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
            
                self.pc += instruction_length
            
            elif ir == SUB:
                self.alu("SUB", operand_a, operand_b)
            
            elif ir == ADD:
                self.alu("ADD", operand_a, operand_b)
            
            elif ir == CALL:
                

            elif ir  == PUSH:
                # Grab the register argument
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]
                # Decrement the sp
                self.reg[SP] -= 1
                # copy the value from the address pointed to by the SP
                self.ram[self.reg[SP]] = val
                self.pc += 2
            elif ir == POP:
                # Grab the value from the top of the stack
                reg = self.ram[self.pc + 1]
                val = self.ram[self.reg[SP]]
                # copy the value from the address pointed to by sp to the given register
                self.reg[reg] = val
                # increment SP
                self.reg[SP] += 1
                self.pc +=2
            elif ir == HLT:
                sys.exit(0)
            else:
                print(f"I did not understand that command: {ir}")
                sys.exit(1)
























# """CPU functionality."""


# LDI = 0b10000010
# HLT = 0b00000001
# PRN = 0b01000111
# MUL = 0b10100010

# import sys


# class CPU:
#     """Main CPU class."""

#     def __init__(self):
#         """Construct a new CPU."""
#         self.reg = [0] * 8
#         self.ram = [0] * 256
#         self.pc = 0
#         self.running = False

#     def ram_write(self, mdr, mar):
#         self.ram[mar] = mdr

#     def ram_read(self, mar):
#         return self.ram[mar]

#     def load(self, filename):
#         """Load a program into memory."""

#         # for now, we've just hardcoded a program
#         try:
#             address = 0

#             with open(filename) as f:
#                 for line in f:
#                     # split before comment
#                     comment_split = line.split('#')

#                     # convert to a number splitting and stripping
#                     num = comment_split[0]. strip()

#                     if num != "":
#                         continue  # ignore blank spaces

#                     val = int(num, 2)

#                     # store val in memory at the address
#                     self.ram[address] = val

#                     address += 1

#         except FileNotFoundError:
#             print(f"{sys.argv[0]}: {filename} not found")
#             sys.exit(2)

#     def alu(self, op, reg_a, reg_b):
#         """ALU operations."""

#         if op == "ADD":
#             self.reg[reg_a] += self.reg[reg_b]

#         elif op == "MUL":
#             self.reg[reg_a] *= self.reg[reg_b]
#         # elif op == "SUB": etc
#         else:
#             raise Exception("Unsupported ALU operation")

#     def trace(self):
#         """
#         Handy function to print out the CPU state. You might want to call this
#         from run() if you need help debugging.
#         """

#         print(f"TRACE: %02X | %02X %02X %02X |" % (
#             self.pc,
#             # self.fl,
#             # self.ie,
#             self.ram_read(self.pc),
#             self.ram_read(self.pc + 1),
#             self.ram_read(self.pc + 2)
#         ), end='')

#         for i in range(8):
#             print(" %02X" % self.reg[i], end='')

#         print()

#     def run(self):
#         """Run the CPU."""
#         while not self.running:
#             ir = self.ram[self.pc]
#             instruction_length = ((ir >> 6) & 0b11) + 1  # (bitshifted instruction)
#             reg_num = self.ram_read(self.pc + 1)
#             print(self.pc)
#             value = self.ram_read(self.pc + 2)
#             # set the instruction length here (extract)

#             # halt
#             if ir == HLT:
#                 self.running = True

#             # LDI
#             elif ir == LDI:
#                 self.reg[reg_num] = value

#             # PRN
#             elif ir == PRN:
#                 print(self.reg[reg_num])

#             elif ir == MUL:
#                 self.alu("MUL", reg_num, value)

#             self.pc += instruction_length

   