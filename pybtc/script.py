import logging

from pybtc.helper import read_varint, little_endian_to_int, int_to_little_endian, encode_varint
from pybtc.opcodes import OP_CODE_FUNCTIONS, OP_CODE_NAMES

LOGGER = logging.getLogger(__name__)


class Script:
    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds

    def raw_serialize(self):
        result = b''
        for cmd in self.cmds:
            if type(cmd) is int:
                result += int_to_little_endian(cmd, 1)
            else:
                length = len(cmd)
                if length < 75:
                    result += int_to_little_endian(length, 1)
                elif 75 < length < 0x100:
                    result += int_to_little_endian(76, 1)
                    result += int_to_little_endian(length, 1)
                elif 0x100 < length < 520:
                    result += int_to_little_endian(77, 1)
                    result += int_to_little_endian(length, 2)
                else:
                    raise ValueError("Too long for a cmd")
                result += cmd
        return result

    def serialize(self):
        result = self.raw_serialize()
        total = len(result)
        return encode_varint(total) + result

    def __add__(self, other):
        return Script(self.cmds + other.cmds)

    def evaluate(self, z):
        cmds = self.cmds[:]
        stack = []
        alt_stack = []
        while len(cmds) > 0:
            cmd = cmds.pop(0)
            if type(cmd) is int:
                operation = OP_CODE_FUNCTIONS[cmd]

                if cmd in (99, 100):
                    if not operation(stack, cmds):
                        LOGGER.info('Bad OP: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
                elif cmd in (107, 108):
                    if not operation(stack, alt_stack):
                        LOGGER.info('Bad OP: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
                elif cmd in (172, 173, 174, 175):
                    if not operation(stack, z):
                        LOGGER.info('Bad OP: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
                else:
                    if not operation(stack):
                        LOGGER.info('Bad OP: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
            else:
                stack.append(cmd)

        if len(stack) == 0 or stack.pop() == b'':
            return False
        return True

    @classmethod
    def parse(cls, s):
        length = read_varint(s)
        cmds = []
        count = 0
        while count < length:
            current = s.read(1)
            count += 1
            current_byte = current[0]
            if 1 <= current_byte <= 75:
                n = current_byte
                cmds.append(s.read(n))
                count += n
            elif current_byte == 76:
                data_length = little_endian_to_int(s.read(1))
                cmds.append(s.read(data_length))
                count += data_length + 1
            elif current_byte == 77:
                data_length = little_endian_to_int(s.read(2))
                cmds.append(s.read(data_length))
                count += data_length + 2
            else:
                op_code = current_byte
                cmds.append(op_code)

        if count != length:
            raise SyntaxError('Parsing script failed')
        return cls(cmds)
