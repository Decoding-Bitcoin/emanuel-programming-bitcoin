from unittest import TestCase

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
