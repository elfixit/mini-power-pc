from bitstring import Bits, BitArray, CreationError
from minipowerpc import BaseOperation, NumBaseOperation, RegisterBaseOperation, NumRegisterBaseOperation

class CLR(RegisterBaseOperation):
    opcodeprefix = (Bits('0b0000'), Bits('0b101'))

    def do(self, op):
        self.register.val = Bits(16)
        self.register.curry = False

class ADD(RegisterBaseOperation):
    opcodeprefix = (Bits('0b0000'), Bits('0b111'))

class ADDD(NumBaseOperation):
    num_length = 15
    num_format = 'int'
    opcodeprefix = Bits('0b1')

    def do(self, opcode):
        opval = opcode[1:len(opcode)].int
        accuval = self.pc.cpu.registers['00'].val.int
        newaccu = accuval + opval
        try:
            accuop = Bits(int=newaccu, length=16)
        except CreationError:
            new_length = len(bin(newaccu))
            accuop = Bits(int=newaccu, length=new_length)
            self.pc.cpu.accu.curry = True
            self.pc.cpu.accu.val = accuop[len(accuop) - 16:]
        else:
            self.pc.cpu.accu.val = accuop

class INC(BaseOperation):
    opcodeprefix = Bits('0b00000001')

class DEC(BaseOperation):
    opcodeprefix = Bits('0b00000100')

class LWDD(NumRegisterBaseOperation):
    num_length = 10
    num_format = 'uint'
    opcodeprefix = (Bits('0b0100'), Bits())

class SWDD(NumRegisterBaseOperation):
    num_length = 10
    num_format = 'uint'
    opcodeprefix = (Bits('0b0110'), Bits())

class SRA(BaseOperation):
    opcodeprefix = Bits('0b00000101')

    def do(self, op):
        self.pc.accu.curry = self.pc.accu.val[len(op)-1]
        self.pc.accu.val = self.pc.accu.val.int >> 1

class SLA(BaseOperation):
    opcodeprefix = Bits('0b00001000')

    def do(self, op):
        self.pc.accu.curry = self.pc.accu.val[1]
        self.pc.accu.val = self.pc.accu.val.int << 1

class SRL(BaseOperation):
    opcodeprefix = Bits('0b00001001')

    def du(self, op):
        self.pc.accu.curry = self.pc.accu.val[len(op)-1]
        self.pc.accu.val = self.pc.accu.val >> 1

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

class BNZ(RegisterBaseOperation):
    opcodeprefix = (Bits('0b0001'), Bits('0b01'))

class BC(RegisterBaseOperation):
    opcodeprefix = (Bits('0b0001'), Bits('0b11'))

class B(RegisterBaseOperation):
    opcodeprefix = (Bits('0b0001'), Bits('0b00'))

class BZD(NumBaseOperation):
    num_length = 10
    num_format = 'uint'
    opcodeprefix = Bits('0b001100')

class BNZD(NumBaseOperation):
    num_length = 10
    num_format = 'uint'
    opcodeprefix = Bits('0b001010')

class BCD(NumBaseOperation):
    num_length = 10
    num_format = 'uint'
    opcodeprefix = Bits('0b001110')

class BD(NumBaseOperation):
    num_length = 10
    num_format = 'uint'
    opcodeprefix = Bits('0b001000')
