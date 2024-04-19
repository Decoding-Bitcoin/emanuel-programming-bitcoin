from pybtc.constants import BASE58_ALPHABET
from pybtc.helper import hash256


def encode_base58(s):
    count = 0
    for c in s:
        if not c:
            count += 1
        else:
            break
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result


def encode_base58_checksum(b):
    return encode_base58(b + hash256(b)[:4])
