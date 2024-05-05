import hashlib
import hmac
from io import BytesIO

from pybtc.constants import *
from pybtc.helper import hash160, big_endian_to_int
from pybtc.base58 import encode_base58_checksum


class FieldElement:
    def __init__(self, num, prime):
        if num >= prime or prime < 0:
            error = 'Num {} not in field range 0 to {}'.format(
                num, prime - 1
            )
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return 'FieldElement_{}({})'.format(self.prime, self.num)

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in different Fields')

        result = (self.num + other.num) % self.prime
        return self.__class__(result, self.prime)

    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add sub numbers in different Fields')

        result = (self.num - other.num) % self.prime
        return self.__class__(result, self.prime)

    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot multiply two numbers in different Fields')

        result = (self.num * other.num) % self.prime
        return self.__class__(result, self.prime)

    def __pow__(self, exponent):
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)

        return self.__class__(num, self.prime)

    def __truediv__(self, other):
        if other.num == 0:
            raise ZeroDivisionError('Cannot divide by zero')

        if self.prime != other.prime:
            raise TypeError('Cannot divide two numbers in different Fields')

        result = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
        return self.__class__(result, self.prime)

    def __rmul__(self, coefficient):
        result = (self.num * coefficient) % self.prime
        return self.__class__(result, self.prime)


class Point:
    def __init__(self, x, y, a, b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        if self.x is None and self.y is None:
            return
        if self.y ** 2 != self.x ** 3 + a * x + b:
            raise ValueError('({}, {}) is not on the curve'.format(x, y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise TypeError('Points {}, {} are not on the same curve'.format(self, other))

        if self.x is None:
            return other
        if other.x is None:
            return self

        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)

        if self == other and self.y == 0 * self.x:
            return self.__class__(None, None, self.a, self.b)

        if self != other:
            slope = (other.y - self.y) / (other.x - self.x)
            x_3 = slope ** 2 - self.x - other.x
            y_3 = slope * (self.x - x_3) - self.y
            return self.__class__(x_3, y_3, self.a, self.b)

        slope = (3 * self.x ** 2 + self.a) / (2 * self.y)
        x_3 = slope ** 2 - 2 * self.x
        y_3 = slope * (self.x - x_3) - self.y
        return self.__class__(x_3, y_3, self.a, self.b)

    def __repr__(self):
        if self.x is None:
            return "{}(inf)".format(self.__class__.__name__)
        if isinstance(self.x, FieldElement):
            return "{}({}, {})_{}_{} FieldElement_{}".format(
                self.__class__.__name__, self.x.num, self.y.num, self.a.num, self.b.num, self.x.prime
            )
        return '{}_({},{})_{}_{}'.format(self.__class__.__name__, self.x, self.y, self.a, self.b)

    def __rmul__(self, coefficient):
        aux_coefficient = coefficient
        current = self
        result = self.__class__(None, None, self.a, self.b)
        while aux_coefficient:
            if aux_coefficient & 1:
                result += current
            current += current
            aux_coefficient >>= 1
        return result


class S256Field(FieldElement):
    def __init__(self, num, prime=None):
        super().__init__(num, P)

    def __repr__(self):
        return '{:x}'.format(self.num).zfill(64)

    def sqrt(self):
        return self ** ((P + 1) // 4)


class S256Point(Point):
    def __init__(self, x, y, a=None, b=None):
        a, b = S256Field(A), S256Field(B)
        if type(x) is int:
            super().__init__(S256Field(x), S256Field(y), a, b)
        else:
            super().__init__(x, y, a, b)

    def __rmul__(self, coefficient):
        aux_coefficient = coefficient % N
        return super().__rmul__(aux_coefficient)

    def verify(self, z, sig):
        g = S256Point(Gx, Gy)
        s_inv = pow(sig.s, N - 2, N)
        u = z * s_inv % N
        v = sig.r * s_inv % N
        total = u * g + v * self
        return total.x.num == sig.r

    def sec(self, compressed=True):
        """returns the binary version of the SEC format"""
        if compressed:
            prefix = 2 + (self.y.num % 2)
            return prefix.to_bytes(1, 'big') + self.x.num.to_bytes(32, 'big')
        else:
            return b'\x04' + self.x.num.to_bytes(32, 'big') + self.y.num.to_bytes(32, 'big')

    @classmethod
    def parse(cls, sec_bin):
        """returns a Point object from a SEC binary (not hex)"""
        if sec_bin[0] == 4:
            x = int.from_bytes(sec_bin[1:33], 'big')
            y = int.from_bytes(sec_bin[33:], 'big')
            return S256Point(x, y)
        is_even = sec_bin[0] == 2
        x = S256Field(int.from_bytes(sec_bin[1:], 'big'))
        alpha = x ** 3 + S256Field(B)
        beta = alpha.sqrt()
        if beta.num % 2:
            even_beta = S256Field(P - beta.num)
            odd_beta = beta
        else:
            even_beta = beta
            odd_beta = S256Field(P - beta.num)
        if is_even:
            return S256Point(x, even_beta)
        else:
            return S256Point(x, odd_beta)

    def hash160(self, compressed=True):
        return hash160(self.sec(compressed))

    def address(self, compressed=True, testnet=False):
        """Returns the address string"""
        h160 = self.hash160(compressed)
        if testnet:
            prefix = b'\x6f'
        else:
            prefix = b'\x00'
        return encode_base58_checksum(prefix + h160)


class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return 'Signature({:x}, {:x})'.format(self.r, self.s)

    def der(self):
        result = self.encode_field(self.r)
        result += self.encode_field(self.s)
        return bytes([0x30, len(result)]) + result

    @classmethod
    def parse(cls, signature_bin):
        s = BytesIO(signature_bin)

        marker = big_endian_to_int(s.read(1))
        if marker != 0x30:
            raise SyntaxError('Invalid signature marker')

        sig_len = big_endian_to_int(s.read(1)) + 2
        if sig_len != len(signature_bin):
            raise SyntaxError('Invalid signature length')

        r_marker = big_endian_to_int(s.read(1))
        if r_marker != 0x02:
            raise SyntaxError('Invalid signature r marker')

        r_length = big_endian_to_int(s.read(1))
        r = big_endian_to_int(s.read(r_length))

        s_marker = big_endian_to_int(s.read(1))
        if s_marker != 0x02:
            raise SyntaxError('Invalid signature s marker')

        s_length = big_endian_to_int(s.read(1))
        s = big_endian_to_int(s.read(s_length))

        total_len = 6 + r_length + s_length
        if total_len != len(signature_bin):
            raise SyntaxError('Invalid signature length')

        return Signature(r, s)

    @staticmethod
    def encode_field(field):
        field = field.to_bytes(32, 'big')
        field = field.lstrip(b'\x00')
        if field[0] & 0x80:
            field = b'\x00' + field
        return bytes([2, len(field)]) + field


class PrivateKey:
    G = S256Point(Gx, Gy)

    def __init__(self, secret):
        self.secret = secret
        self.point = secret * self.G

    def hex(self):
        return '{:x}'.format(self.secret).zfill(64)

    def sign(self, z):
        k = self.deterministic_k(z)
        r = (k * self.G).x.num
        k_inv = pow(k, N - 2, N)
        s = (z + r * self.secret) * k_inv % N
        if s > N / 2:
            s = N - s
        return Signature(r, s)

    def deterministic_k(self, z):
        k = b'\x00' * 32
        v = b'\x01' * 32
        if z > N:
            z -= N
        z_bytes = z.to_bytes(32, 'big')
        secret_bytes = self.secret.to_bytes(32, 'big')
        s256 = hashlib.sha256
        k = hmac.new(k, v + b'\x00' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b'\x01' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            candidate = int.from_bytes(v, 'big')
            if 1 <= candidate < N:
                return candidate
            k = hmac.new(k, v + b'\x00', s256).digest()
            v = hmac.new(k, v, s256).digest()

    def wif(self, compressed=True, testnet=False):
        secret_bytes = self.secret.to_bytes(32, 'big')

        if testnet:
            prefix = b'\xef'
        else:
            prefix = b'\x80'

        if compressed:
            suffix = b'\x01'
        else:
            suffix = b''

        return encode_base58_checksum(prefix + secret_bytes + suffix)
