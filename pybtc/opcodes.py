import hashlib
from ripemd import ripemd160

from pybtc.helper import hash256, hash160
from pybtc.ecc import S256Point, Signature


def encode_num(num):
    if num == 0:
        return b''
    abs_num = abs(num)
    negative = num < 0
    result = bytearray()

    while abs_num:
        result.append(abs_num & 0xff)
        abs_num >>= 8

    if result[-1] * 0x80:
        if negative:
            result.append(0x80)
        else:
            result.append(0)
    elif negative:
        result[-1] |= 0x80

    return bytes(result)


def decode_num(element):
    if element == b'':
        return 0

    big_endian = element[::-1]

    if big_endian[0] & 0x80:
        negative = True
        result = big_endian[0] & 0x7f
    else:
        negative = False
        result = big_endian[0]

    for c in big_endian[1:]:
        result <<= 8
        result += c

    if negative:
        return -result

    return result


def op_0(stack):
    stack.append(encode_num(0))
    return True


def op_1negate(stack):
    stack.append(encode_num(-1))
    return True


def op_1(stack):
    stack.append(encode_num(1))
    return True


def op_2(stack):
    stack.append(encode_num(2))
    return True


def op_3(stack):
    stack.append(encode_num(3))
    return True


def op_4(stack):
    stack.append(encode_num(4))
    return True


def op_5(stack):
    stack.append(encode_num(5))
    return True


def op_6(stack):
    stack.append(encode_num(6))
    return True


def op_7(stack):
    stack.append(encode_num(7))
    return True


def op_8(stack):
    stack.append(encode_num(8))
    return True


def op_9(stack):
    stack.append(encode_num(9))
    return True


def op_10(stack):
    stack.append(encode_num(10))
    return True


def op_11(stack):
    stack.append(encode_num(11))
    return True


def op_12(stack):
    stack.append(encode_num(12))
    return True


def op_13(stack):
    stack.append(encode_num(13))
    return True


def op_14(stack):
    stack.append(encode_num(14))
    return True


def op_15(stack):
    stack.append(encode_num(15))
    return True


def op_16(stack):
    stack.append(encode_num(16))
    return True


def op_nop(stack):
    return True


def op_verify(stack):
    if len(stack) == 0:
        return False

    element = stack.pop()
    if decode_num(element) == 0:
        return False
    return True


def op_return(stack):
    return False


def op_toaltstack(stack, alt_stack):
    if len(stack) == 0:
        return False

    alt_stack.append(stack.pop())
    return True


def op_fromaltstack(stack, alt_stack):
    if len(alt_stack) == 0:
        return False

    stack.append(alt_stack.pop())
    return True


def op_ifdup(stack):
    if len(stack) == 0:
        return False

    top_of_stack = stack[-1]
    if decode_num(top_of_stack) != 0:
        stack.append(top_of_stack)
    return True


def op_depth(stack):
    stack.append(encode_num(len(stack)))
    return True


def op_drop(stack):
    if len(stack) == 0:
        return False

    stack.pop()
    return True


def op_dup(stack):
    if len(stack) == 0:
        return False

    stack.append(stack[-1])
    return True


def op_nip(stack):
    if len(stack) < 2:
        return False

    top_of_stack = stack.pop()
    stack.pop()
    stack.append(top_of_stack)
    return True


def op_over(stack):
    if len(stack) < 2:
        return False

    second_to_top_of_stack = stack[-2]
    stack.append(second_to_top_of_stack)
    return True


def op_pick(stack):
    if len(stack) == 0:
        return False

    n = decode_num(stack.pop())
    if len(stack) < n + 1:
        return False

    nth_item = stack[n]
    stack.append(nth_item)
    return True


def op_roll(stack):
    if len(stack) == 0:
        return False

    n = decode_num(stack.pop())
    if len(stack) < n + 1:
        return False

    nth_item = stack.pop(n)
    stack.append(nth_item)
    return True


def op_rot(stack):
    if len(stack) < 3:
        return False

    stack.append(stack.pop(-3))
    return True


def op_swap(stack):
    if len(stack) < 2:
        return False

    aux = stack[-1]
    stack[-1] = stack[-2]
    stack[-2] = aux
    return True


def op_tuck(stack):
    if len(stack) < 2:
        return False

    top = stack.pop()
    second_to_top = stack.pop()
    stack.append(top)
    stack.append(second_to_top)
    stack.append(top)
    return True


def op_2drop(stack):
    if len(stack) < 2:
        return False

    stack.pop()
    stack.pop()
    return True


def op_2dup(stack):
    if len(stack) < 2:
        return False

    top = stack[-1]
    second_to_top = stack[-2]
    stack.append(second_to_top)
    stack.append(top)
    return True


def op_3dup(stack):
    if len(stack) < 3:
        return False

    top = stack[-1]
    second_to_top = stack[-2]
    third_to_top = stack[-3]
    stack.append(third_to_top)
    stack.append(second_to_top)
    stack.append(top)
    return True


def op_2over(stack):
    if len(stack) < 4:
        return False

    third_to_top = stack[-3]
    fourth_to_top = stack[-4]
    stack.append(fourth_to_top)
    stack.append(third_to_top)
    return True


def op_2rot(stack):
    if len(stack) < 6:
        return False

    top = stack.pop()
    second_to_top = stack.pop()
    third_to_top = stack.pop()
    fourth_to_top = stack.pop()
    fifth_to_top = stack.pop()
    sixth_to_top = stack.pop()
    stack.append(fourth_to_top)
    stack.append(third_to_top)
    stack.append(second_to_top)
    stack.append(top)
    stack.append(sixth_to_top)
    stack.append(fifth_to_top)
    return True


def op_2swap(stack):
    if len(stack) < 4:
        return False

    aux = stack[-1]
    stack[-1] = stack[-3]
    stack[-3] = aux

    aux = stack[-2]
    stack[-2] = stack[-4]
    stack[-4] = aux
    return True


def op_size(stack):
    if len(stack) == 0:
        return False

    string = stack[-1]
    stack.append(encode_num(len(string)))
    return True


def op_equal(stack):
    if len(stack) < 2:
        return False

    top = stack.pop()
    second_to_top = stack.pop()
    if top == second_to_top:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True


def op_equalverify(stack):
    return op_equal(stack) and op_verify(stack)


def op_1add(stack):
    if len(stack) == 0:
        return False

    element = decode_num(stack.pop())
    stack.append(encode_num(element + 1))
    return True


def op_1sub(stack):
    if len(stack) == 0:
        return False

    element = decode_num(stack.pop())
    stack.append(encode_num(element - 1))
    return True


def op_negate(stack):
    if len(stack) == 0:
        return False

    element = decode_num(stack.pop())
    stack.append(encode_num(element * -1))
    return True


def op_abs(stack):
    if len(stack) == 0:
        return False

    element = decode_num(stack.pop())
    stack.append(encode_num(abs(element)))
    return True


def op_not(stack):
    if len(stack) == 0:
        return False

    element = decode_num(stack.pop())
    if element == 0:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True


def op_0notequal(stack):
    if len(stack) == 0:
        return False

    element = decode_num(stack.pop())
    if element == 0:
        stack.append(encode_num(0))
    else:
        stack.append(encode_num(1))
    return True


def op_add(stack):
    if len(stack) < 2:
        return False

    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    stack.append(encode_num(element1 + element2))
    return True


def op_sub(stack):
    if len(stack) < 2:
        return False

    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    stack.append(encode_num(element1 - element2))
    return True


def op_mul(stack):
    if len(stack) < 2:
        return False

    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    stack.append(encode_num(element1 * element2))
    return True


def op_booland(stack):
    if len(stack) < 2:
        return False

    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element1 != 0 and element2 == 0:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True


def op_boolor(stack):
    if len(stack) < 2:
        return False

    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element1 != 0 or element2 != 0:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True


def op_numequal(stack):
    if len(stack) < 2:
        return False

    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element1 == element2:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True


def op_numequalverify(stack):
    return op_numequal(stack) and op_verify(stack)


def op_numnotequal(stack):
    if len(stack) < 2:
        return False

    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element1 != element2:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True


def op_lessthan(stack):
    if len(stack) < 2:
        return False

    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element2 < element1:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True


def op_greaterthan(stack):
    if len(stack) < 2:
        return False

    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element2 > element1:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True


def op_lessthanorequal(stack):
    if len(stack) < 2:
        return False

    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element2 <= element1:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True


def op_greaterthanorequal(stack):
    if len(stack) < 2:
        return False

    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element2 >= element1:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True


def op_min(stack):
    if len(stack) < 2:
        return False

    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element2 < element1:
        stack.append(encode_num(element2))
    else:
        stack.append(encode_num(element1))
    return True


def op_max(stack):
    if len(stack) < 2:
        return False

    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element2 > element1:
        stack.append(encode_num(element2))
    else:
        stack.append(encode_num(element1))
    return True


def op_within(stack):
    if len(stack) < 3:
        return False

    max_value = decode_num(stack.pop())
    min_value = decode_num(stack.pop())
    value = decode_num(stack.pop())
    if min_value >= value > max_value:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True


def op_ripemd160(stack):
    if len(stack) == 0:
        return False

    element = stack.pop()
    hashed_element = ripemd160.new(element).digest()
    stack.append(hashed_element)
    return True


def op_sha1(stack):
    if len(stack) == 0:
        return False

    element = stack.pop()
    hashed_element = hashlib.sha1(element).digest()
    stack.append(hashed_element)
    return True


def op_sha256(stack):
    if len(stack) == 0:
        return False

    element = stack.pop()
    hashed_element = hashlib.sha256(element).digest()
    stack.append(hashed_element)
    return True


def op_hash160(stack):
    if len(stack) == 0:
        return False
    element = stack.pop()
    stack.append(hash160(element))
    return True


def op_hash256(stack):
    if len(stack) == 0:
        return False
    element = stack.pop()
    stack.append(hash256(element))
    return True


def op_checksig(stack, z):
    if len(stack) < 2:
        return False

    pub_key = S256Point.parse(stack.pop())
    sig = Signature.parse(stack.pop())
    if pub_key.verify(z, sig):
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True


def op_checksigverify(stack, z):
    return op_checksig(stack, z) and op_verify(stack)


OP_CODE_FUNCTIONS = {
    0x00: op_0,
    0x4f: op_1negate,
    0x51: op_1,
    0x52: op_2,
    0x53: op_3,
    0x54: op_4,
    0x55: op_5,
    0x56: op_6,
    0x57: op_7,
    0x58: op_8,
    0x59: op_9,
    0x5a: op_10,
    0x5b: op_11,
    0x5c: op_12,
    0x5d: op_13,
    0x5e: op_14,
    0x5f: op_15,
    0x60: op_16,
    0x61: op_nop,
    0x69: op_verify,
    0x6a: op_return,
    0x6b: op_toaltstack,
    0x6c: op_fromaltstack,
    0x6d: op_2drop,
    0x6e: op_2dup,
    0x6f: op_3dup,
    0x70: op_2over,
    0x71: op_2rot,
    0x72: op_2swap,
    0x73: op_ifdup,
    0x74: op_depth,
    0x75: op_drop,
    0x76: op_dup,
    0x77: op_nip,
    0x78: op_over,
    0x79: op_pick,
    0x7a: op_roll,
    0x7b: op_rot,
    0x7c: op_swap,
    0x7d: op_tuck,
    0x82: op_size,
    0x87: op_equal,
    0x88: op_equalverify,
    0x8b: op_1add,
    0x8c: op_1sub,
    0x8f: op_negate,
    0x90: op_abs,
    0x91: op_not,
    0x92: op_0notequal,
    0x93: op_add,
    0x94: op_sub,
    0x95: op_mul,
    0x9a: op_booland,
    0x9b: op_boolor,
    0x9c: op_numequal,
    0x9d: op_numequalverify,
    0x9e: op_numnotequal,
    0x9f: op_lessthan,
    0xa0: op_greaterthan,
    0xa1: op_lessthanorequal,
    0xa2: op_greaterthanorequal,
    0xa3: op_min,
    0xa4: op_max,
    0xa5: op_within,
    0xa6: op_ripemd160,
    0xa7: op_sha1,
    0xa8: op_sha256,
    0xa9: op_hash160,
    0xaa: op_hash256,
    0xac: op_checksig,
    0xad: op_checksigverify,
}

OP_CODE_NAMES = {
    0x00: 'OP_O',
    0x4f: 'OP_1NEGATE',
    0x51: 'OP_1',
    0x52: 'OP_2',
    0x53: 'OP_3',
    0x54: 'OP_4',
    0x55: 'OP_5',
    0x56: 'OP_6',
    0x57: 'OP_7',
    0x58: 'OP_8',
    0x59: 'OP_9',
    0x5a: 'OP_10',
    0x5b: 'OP_11',
    0x5c: 'OP_12',
    0x5d: 'OP_13',
    0x5e: 'OP_14',
    0x5f: 'OP_15',
    0x60: 'OP_16',
    0x61: 'OP_NOP',
    0x69: 'OP_VERIFY',
    0x6a: 'OP_RETURN',
    0x6b: 'OP_TOALTSTACK',
    0x6c: 'OP_FROMALTSTACK',
    0x6d: 'OP_2DROP',
    0x6e: 'OP_2DUP',
    0x6f: 'OP_3DUP',
    0x70: 'OP_2OVER',
    0x71: 'OP_2ROT',
    0x72: 'OP_2SWAP',
    0x73: 'OP_IFDUP',
    0x74: 'OP_DEPTH',
    0x75: 'OP_DROP',
    0x76: 'OP_DUP',
    0x77: 'OP_NIP',
    0x78: 'OP_OVER',
    0x79: 'OP_PICK',
    0x7a: 'OP_ROLL',
    0x7b: 'OP_ROT',
    0x7c: 'OP_SWAP',
    0x7d: 'OP_TUCK',
    0x82: 'OP_SIZE',
    0x87: 'OP_EQUAL',
    0x88: 'OP_EQUALVERIFY',
    0x8b: 'OP_1ADD',
    0x8c: 'OP_1SUB',
    0x8f: 'OP_NEGATE',
    0x90: 'OP_ABS',
    0x91: 'OP_NOT',
    0x92: 'OP_0NOTEQUAL',
    0x93: 'OP_ADD',
    0x94: 'OP_SUB',
    0x95: 'OP_MUL',
    0x9a: 'OP_BOOLAND',
    0x9b: 'OP_BOOLOR',
    0x9c: 'OP_NUMEQUAL',
    0x9d: 'OP_NUMEQUALVERIFY',
    0x9e: 'OP_NUMNOTEQUAL',
    0x9f: 'OP_LESSTHAN',
    0xa0: 'OP_GREATERTHAN',
    0xa1: 'OP_LESSTHANORQUAL',
    0xa2: 'OP_GREATERTHANORQUAL',
    0xa3: 'OP_MIN',
    0xa4: 'OP_MAX',
    0xa5: 'OP_WITHIN',
    0xa6: 'OP_RIPEMP160',
    0xa7: 'OP_SHA1',
    0xa8: 'OP_SHA256',
    0xa9: 'OP_HASH160',
    0xaa: 'OP_HASH256',
    0xac: 'OP_CHECKSIG',
}
