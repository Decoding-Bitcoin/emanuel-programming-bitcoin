import hashlib
import hmac
from random import randint

from pybtc.constants import *


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


class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return 'Signature({:x}, {:x})'.format(self.r, self.s)


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


