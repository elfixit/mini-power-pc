from bitstring import Bits, BitArray, CreationError
from minipowerpc import BaseOperation, NumBaseOperation, RegisterBaseOperation, NumRegisterBaseOperation
from minipowerpc.utils import set_newval
class CLR(RegisterBaseOperation):
    opcodeprefix = (Bits('0b0000'), Bits('0b101'))

    def do(self, op):
        self.register.val = Bits(16)
        self.register.curry = False

class ADD(RegisterBaseOperation):
    opcodeprefix = (Bits('0b0000'), Bits('0b111'))

    def do(self, op):
        regval = self.register.val.int
        accuval = self.pc.cpu.accu.val.int
        newval = regval + accuval
        set_newval(self.pc, newval)

class ADDD(NumBaseOperation):
    num_length = 15
    num_format = 'int'
    opcodeprefix = Bits('0b1')

    def do(self, opcode):
        opval = opcode[1:len(opcode)].int
        accuval = self.pc.cpu.registers['00'].val.int
        newaccu = accuval + opval
        set_newval(self.pc, newaccu)

class INC(BaseOperation):
    opcodeprefix = Bits('0b00000001')

    def do(self, opcode):
        newaccu = self.pc.cpu.accu.val.int + 1
        set_newval(self.pc, newaccu)

class DEC(BaseOperation):
    opcodeprefix = Bits('0b00000100')

    def do(self, opcode):
        newaccu = self.pc.cpu.accu.val.int - 1
        set_newval(self.pc, newaccu)

class LWDD(NumRegisterBaseOperation):
    num_length = 10
    num_format = 'uint'
    opcodeprefix = (Bits('0b0100'), Bits())

    def do(self, op):
        pos = op[6:16].uint
        self.register.val = self.pc.cpu.mem.get(pos)

class SWDD(NumRegisterBaseOperation):
    num_length = 10
    num_format = 'uint'
    opcodeprefix = (Bits('0b0110'), Bits())

    def do(self, op):
        pos = op[6:16].uint
        self.pc.cpu.mem.set(pos, self.register.val)

class SRA(BaseOperation):
    opcodeprefix = Bits('0b00000101')

    def do(self, op):
        self.pc.cpu.accu.curry = self.pc.cpu.accu.val[len(op)-1]
        self.pc.cpu.accu.val = BitArray(self.pc.cpu.accu.val)
        self.pc.cpu.accu.val[1:len(op)] = self.pc.cpu.accu.val[1:len(op)] >> 1

class SLA(BaseOperation):
    opcodeprefix = Bits('0b00001000')

    def do(self, op):
        self.pc.cpu.accu.curry = self.pc.cpu.accu.val[1]
        self.pc.cpu.accu.val = BitArray(self.cpu.accu.val)
        self.pc.cpu.accu.val[1:len(op)] = self.pc.cpu.accu.val[1:len(op)] << 1

class SRL(BaseOperation):
    opcodeprefix = Bits('0b00001001')

    def do(self, op):
        self.pc.cpu.accu.curry = self.pc.cpu.accu.val[len(op)-1]
        self.pc.cpu.accu.val = self.pc.cpu.accu.val >> 1

class SLL(BaseOperation):
    opcodeprefix = Bits('0b00001100')

    def do(self, op):
        self.pc.accu.curry = self.pc.accu.val[0]
        self.pc.accu.val = self.pc.accu.val << 1

class AND(RegisterBaseOperation):
    opcodeprefix = (Bits('0b0000'), Bits('0b100'))

    def do(self, op):
        self.pc.accu.val = self.pc.accu.val & self.register.val

class OR(RegisterBaseOperation):
    opcodeprefix = (Bits('0b0000'), Bits('0b110'))

    def do(self, op):
        self.pc.accu.val = self.pc.accu.val | self.register.val

class NOT(BaseOperation):
    opcodeprefix = Bits('0b000000001')

    def do(self, op):
        self.pc.accu.val = ~self.pc.accu.val

class BZ(RegisterBaseOperation):
    opcodeprefix = (Bits('0b0001'), Bits('0b10'))

    def do(self, op):
        if self.pc.cpu.accu.val.int == 0:
            self.pc.cpu.mem.jump(self.register.val.uint)

class BNZ(RegisterBaseOperation):
    opcodeprefix = (Bits('0b0001'), Bits('0b01'))

    def do(self, op):
        if not self.pc.cpu.accu.val.int == 0:
            self.pc.cpu.mem.jump(self.register.val.uint)

class BC(RegisterBaseOperation):
    opcodeprefix = (Bits('0b0001'), Bits('0b11'))

    def do(self, op):
        if self.pc.cpu.accu.curry:
            self.pc.cpu.mem.jump(self.register.val.uint)

class B(RegisterBaseOperation):
    opcodeprefix = (Bits('0b0001'), Bits('0b00'))

    def do(self, op):
        self.pc.cpu.mem.jump(self.register.val.uint)

class BZD(NumBaseOperation):
    num_length = 10
    num_format = 'uint'
    opcodeprefix = Bits('0b001100')

    def do(self, op):
       if self.pc.cpu.accu.val.int == 0:
           start = len(op) - self.num_length
           num = getattr(op, self.num_format, 0)
           self.pc.cpu.mem.jump(num)

class BNZD(NumBaseOperation):
    num_length = 10
    num_format = 'uint'
    opcodeprefix = Bits('0b001010')

    def do(self, op):
        if not self.pc.cpu.accu.val.int == 0:
            start = len(op) - self.num_length
            num = getattr(op[start:len(op)], self.num_format, 0)
            self.pc.cpu.mem.jump(num)

class BCD(NumBaseOperation):
    num_length = 10
    num_format = 'uint'
    opcodeprefix = Bits('0b001110')

    def do(self, op):
        if self.pc.cpu.accu.curry:
            start = len(op) - self.num_length
            num = getattr(op[start:len(op)], self.num_format, 0)
            self.pc.cpu.mem.jump(num)


class BD(NumBaseOperation):
    num_length = 10
    num_format = 'uint'
    opcodeprefix = Bits('0b001000')

    def do(self, op):
        start = len(op) - self.num_length
        num = getattr(op[start:len(op)], self.num_format, 0)
        self.pc.cpu.mem.jump(num)

