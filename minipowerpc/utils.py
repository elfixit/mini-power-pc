from bitstring import Bits, BitArray

def get_number(num_str, length=15, format="int"):
    return Bits("{}:{}={}".format(format, length, num_str))

def get_reference(num_str, length=10, format="uint"):
    if num_str.startswith('C') or num_str.startswith('c'):
        num_str.replace('C', '1')
        num_str.replace('c', '1')
    elif num_str.startswith('M') or num_str.startswith('m'):
        num_str.replace('M', '5')
        num_str.replace('m', '5')
    return get_number(num_str, length, format)

from bitstring import CreationError

def set_newval(pc, newaccu):
    try:
        accuop = Bits(int=newaccu, length=16)
    except CreationError:
        new_length = len(bin(newaccu))
        accuop = Bits(int=newaccu, length=new_length)
        pc.cpu.accu.curry = True
        pc.cpu.accu.val = accuop[len(accuop) - 16:]
    else:
        pc.cpu.accu.val = accuop

