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
