import struct

from math import log, ceil, isnan

# NOTE: this two function may not do the same thing as what deepcool does
#       but it appears to be the intent so I'm taking shortcuts

def u32_to_bytes(number, octets=1):
    """convert uint32 into list of ints/bytes with specified length in 1-4 octets"""
    if not (1 <= octets <= 4):
        raise ValueError('result length is out of range (1-4 allowed)')

    int_octets = [b for b in struct.pack('>I', number)]

    return int_octets[-octets:]

def f32_to_bytes(number):
    if isnan(number):
        raise ValueError('NaN is not a valid value to convert')

    if number == 0:
        return [0, 0, 0, 0]

    return  [b for b in struct.pack('>f', number)]
