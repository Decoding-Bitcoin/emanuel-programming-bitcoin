from unittest import TestCase
from io import BytesIO

from pybtc.helper import *


class HelperTest(TestCase):
    def test_int_to_little_endian(self):
        n1 = 3921
        le1 = 0xF51.to_bytes(2, 'little')
        self.assertEqual(int_to_little_endian(n1, 2), le1)

        n2 = 1346134
        le2 = 0x148A56.to_bytes(8, 'little')
        self.assertEqual(int_to_little_endian(n2, 8), le2)
        self.assertFalse(int_to_little_endian(n1, 8) == le2)

    def test_little_endian_to_int(self):
        n1 = 19847
        le1 = 0x4D87.to_bytes(4, 'little')
        self.assertEqual(little_endian_to_int(le1), n1)

        n2 = 609713460971
        le2 = 0x8DF5C116EB.to_bytes(18, 'little')
        self.assertEqual(little_endian_to_int(le2), n2)
        self.assertFalse(little_endian_to_int(le2) == n1)

    def test_read_var_int(self):
        n1 = 0x64.to_bytes(1)
        vi1 = BytesIO(n1)
        self.assertEqual(read_varint(vi1),100)

        n2 = 0xfdff00.to_bytes(3)
        vi2 = BytesIO(n2)
        self.assertEqual(read_varint(vi2), 255)

        n3 = 0xfd2b02.to_bytes(3)
        vi3 = BytesIO(n3)
        self.assertEqual(read_varint(vi3), 555)

        n4 = 0xfe7f110100.to_bytes(5)
        vi4 = BytesIO(n4)
        self.assertEqual(read_varint(vi4), 70015)

        n5 = 0xff6dc7ed3e60100000.to_bytes(9)
        vi5 = BytesIO(n5)
        self.assertEqual(read_varint(vi5), 18005558675309)

        vi6 = BytesIO(n3)
        self.assertFalse(read_varint(vi6) == 255)

    def test_encode_varint(self):
        n1 = 100
        encoded_1 = 0x64.to_bytes(1)
        self.assertEqual(encode_varint(n1), encoded_1)

        n2 = 255
        encoded_2 = 0xfdff00.to_bytes(3)
        self.assertEqual(encode_varint(n2), encoded_2)

        n3 = 555
        encoded_3 = 0xfd2b02.to_bytes(3)
        self.assertEqual(encode_varint(n3), encoded_3)

        n4 = 70015
        encoded_4 = 0xfe7f110100.to_bytes(5)
        self.assertEqual(encode_varint(n4), encoded_4)

        n5 = 18005558675309
        encoded_5 = 0xff6dc7ed3e60100000.to_bytes(9)
        self.assertEqual(encode_varint(n5), encoded_5)

        self.assertFalse(encode_varint(n2) == n3)

        with self.assertRaises(ValueError):
            n6 = 0x10000000000000000
            encode_varint(n6)
