import inspect
import copy
from bitstring import Bits, BitArray, BitStream
from minipowerpc.utils import get_reference, get_number

class Register(object):
    def __init__(self):
        self.curry = False
        self.val = BitArray(16)

class Mem(object):
    def __init__(self):
        self.real = BitStream(600*16)
        self.jumps = 0

    def load(self, file):
        self.real = BitStream(filename=file)

    def save(self, file):
        self.real.tofile(file)

    def jump(self, pos):
        self.jumps += 1
        self.real.bytepos = pos

    def read(self, size=16):
        return self.real.read(16)

    def get(self, pos, size=16):
        realpos = pos * 8
        return self.real[realpos:realpos+size]

    def set(self, pos, bits):
        realpos = pos * 8
        self.real[realpos:realpos+len(bits)] = bits

    @property
    def pos(self):
        return self.real.bytepos


class CPU(object):

    END = BitArray(16)

    def __init__(self):
        self.debug = False
        self.mem = Mem()
        self.mem.jump(100)
        self.exec_time_real = 0
        self.steps = 0
        self._ended = False
        self.reg_ids = [BitArray('0b00'), BitArray('0b01'), BitArray('0b10'), BitArray('0b11')]
        self.registers = {
            '00': Register(),
            '01': Register(),
            '10': Register(),
            '11': Register()
        }
        self._opcodeprefixes = {}

    @property
    def accu(self):
        return self.registers['00']

    def register_opcodeprefix(self, prefix, operation):
        if not prefix in self._opcodeprefixes.keys():
            self._opcodeprefixes[prefix] = operation
        else:
            raise Exception("OpCode prefix allready registered")

    def get_operation(self, op):
        for prefix in self._opcodeprefixes.keys():
            if op.startswith(BitArray(bin=prefix)):
                if self.debug:
                    print "execute opcode:{} with prefix: {} object: {}".format(op.bin, prefix,
                                                                                self._opcodeprefixes[prefix])
                return self._opcodeprefixes[prefix]

    def init(self):
        self._ended = False
        self.mem.jump(100)
        self.exec_time_real = 0

    def step(self):
        if not self.end:
            op = self.mem.read()
            if op == self.END:
                self._ended = True
            else:
                self.get_operation(op).do(op)
                self.steps += 1


    def run(self):
        while not self.end:
            self.step()

    @property
    def end(self):
        return self._ended

class Compiler(object):
    def __init__(self):
        self._mnemonics = {}
        self.debug = False

    def register_mnemonic(self, action, cls):
        print "register: action={} cls={}".format(action,cls)
        self._mnemonics[action] = cls

    def compile_str(self, mnemonicstr):
        opcode_all = BitArray(100*8)
        for line in mnemonicstr.splitlines():
            elements = line.split()
            if not len(elements) == 0 and not line.startswith(';'):
                cls = self._mnemonics[elements.pop(0)]
                opcode = cls.compile(*elements)
                if self.debug:
                    print "compiled line: {} to: {}".format(line, opcode.bin)
                if not len(opcode) == 16:
                        raise Exception("Invalid opcode compiling.. {}")
                opcode_all.append(opcode)
            else:
                opcode_all.append(Bits(16))
        opcode_final = BitArray(600*8)
        opcode_final[0:len(opcode_all)] = opcode_all
        return opcode_final

    def compile(self, file, file_out=None):
        if file_out == None:
            file_out = file.rpartition('.')[0]  + ".mippc"
        fp_in = open(file, 'r')
        mnemonic = fp_in.read()
        opcode = self.compile_str(mnemonic)
        fp_out = open(file_out, "wb")
        opcode.tofile(fp_out)
        return file_out


class MiniPC(object):
    def __init__(self):
        self.cpu = CPU()
        self.compiler = Compiler()
        from minipowerpc import operations
        for key, value in dict(operations.__dict__).items():
            if inspect.isclass(value) and issubclass(value, BaseOperation):
                if not value in (BaseOperation, NumBaseOperation, RegisterBaseOperation, NumRegisterBaseOperation):
                    print "register {}".format(key)
                    value.register(self)

    def setDebug(self, debug=True):
        self.compiler.debug = debug
        self.cpu.debug = debug


    def register_mnemonic(self, action, cls):
        self.compiler.register_mnemonic(action, cls)

    def register_opcode(self, prefix, operation):
        self.cpu.register_opcodeprefix(prefix, operation)

class BaseOperation(object):

    @classmethod
    def __repr__(cls):
        if getattr(cls, 'opcodeprefix', False):
            return "{}: {}".format(cls.__name__, cls.opcodeprefix)

    @classmethod
    def register(cls, pc):
        pc.register_mnemonic(cls.__name__, cls)
        pc.register_opcode(cls.opcodeprefix.bin, cls(pc))

    @classmethod
    def compile(cls, *args):
        compiled = BitArray(16)
        compiled[0:len(cls.opcodeprefix)] = cls.opcodeprefix
        return compiled

    def __init__(self, pc):
        self.pc = pc

    def decompile(self, opcode):
        return self.__class__.__name__

class NumBaseOperation(BaseOperation):
    num_length=10
    @classmethod
    def compile(cls, *args):
        num = get_reference(args[0], length=cls.num_length, format=cls.num_format)
        compiled = BitArray(16)
        prelen = len(cls.opcodeprefix)
        compiled[0:prelen] = cls.opcodeprefix
        compiled[prelen:prelen+cls.num_length] = num
        return compiled


class RegisterBaseOperation(BaseOperation):

    @classmethod
    def register(cls, pc):
        pc.register_mnemonic(cls.__name__, cls)
        for reg in pc.cpu.reg_ids:
            prefix = cls.opcodeprefix[0].bin
            prefix += reg.bin
            prefix += cls.opcodeprefix[1].bin
            pc.register_opcode(prefix, cls(pc, pc.cpu.registers[reg.bin]))
            del prefix

    @classmethod
    def compile(cls, *args):
        compiled = BitArray(16)
        len_prefix0 = len(cls.opcodeprefix[0])
        len_prefix1 = len(cls.opcodeprefix[1])
        compiled[0:len_prefix0] = cls.opcodeprefix[0]
        compiled[len_prefix0:len_prefix0+2] = BitArray(bin=args[0])
        compiled[len_prefix0+2:len_prefix0+2+len_prefix1] = cls.opcodeprefix[1]
        return compiled

    def __init__(self, pc, register):
        self.register = register
        super(RegisterBaseOperation, self).__init__(pc)

class NumRegisterBaseOperation(RegisterBaseOperation):
    @classmethod
    def compile(cls, *args):
        len_start = len(cls.opcodeprefix[0])
        len_end = len(cls.opcodeprefix[1])
        num = BitArray(uint=int(args[1]), length=10)
        reg = BitArray(bin=args[0])
        compiled = BitArray(16)
        compiled[0:len_start] = cls.opcodeprefix[0]
        compiled[len_start:len_start+len(reg)] = reg
        compiled[len_start+len(reg):len_start+len(reg)+len_end] = cls.opcodeprefix[1]
        compiled[6:16] = get_reference(args[1], length=cls.num_length, format=cls.num_format)
        return compiled

