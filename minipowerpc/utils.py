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


