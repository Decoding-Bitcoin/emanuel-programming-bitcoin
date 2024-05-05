import hashlib
from ripemd import ripemd160


def hash160(s):
    """sha256 followed by ripemd160"""
    return ripemd160.new(hashlib.sha256(s).digest()).digest()


def hash256(s):
    """two rounds of sha256"""
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


def little_endian_to_int(b):
    return int.from_bytes(b, 'little')


def int_to_little_endian(i, size):
    return i.to_bytes(size, 'little')


def big_endian_to_int(b):
    return int.from_bytes(b, 'big')


def int_to_big_endian(i, size):
    return i.to_bytes(size, 'big')


def read_varint(s):
    """read_varint reads a variable integer from a stream"""
    i = s.read(1)[0]
    if i == 0xfd:
        # 0xfd means the next two bytes are the number
        return little_endian_to_int(s.read(2))
    elif i == 0xfe:
        # 0xfe means the next four bytes are the number
        return little_endian_to_int(s.read(4))
    elif i == 0xff:
        # 0xff means the next eight bytes are the number
        return little_endian_to_int(s.read(8))
    else:
        # anything else if just the integer
        return i


def encode_varint(i):
    """encodes an integer as a varint"""
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        return b'\xfd' + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        return b'\xfe' + int_to_little_endian(i, 4)
    elif i < 0x10000000000000000:
        return b'\xff' + int_to_little_endian(i, 8)
    else:
        raise ValueError('Integer too large {}'.format(i))
