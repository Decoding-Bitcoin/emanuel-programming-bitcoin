from unittest import TestCase
from pybtc.ecc import *
from pybtc.constants import Gx, Gy


class FieldElementTest(TestCase):
    def test_initialize(self):
        with self.assertRaises(ValueError):
            fe1 = FieldElement(13, 13)
        with self.assertRaises(ValueError):
            fe2 = FieldElement(1, -13)

    def test_eq(self):
        fe_10_13_a = FieldElement(10, 13)
        fe_10_13_b = FieldElement(10, 13)
        fe_6_13 = FieldElement(6, 13)
        fe_6_11 = FieldElement(6, 11)
        self.assertEqual(fe_10_13_a, fe_10_13_b)
        self.assertFalse(fe_10_13_a == fe_6_13)
        self.assertFalse(fe_6_13 == fe_6_11)

    def test_ne(self):
        fe_10_13_a = FieldElement(10, 13)
        fe_10_13_b = FieldElement(10, 13)
        fe_6_13 = FieldElement(6, 13)
        fe_6_11 = FieldElement(6, 11)
        self.assertTrue(fe_10_13_a != fe_6_13)
        self.assertFalse(fe_10_13_a != fe_10_13_b)
        self.assertTrue(fe_6_13 != fe_6_11)

    def test_add(self):
        fe_7_19 = FieldElement(7, 19)
        fe_11_19 = FieldElement(11, 19)
        fe_12_19 = FieldElement(12, 19)
        fe_0_19 = FieldElement(0, 19)
        fe_18_19 = FieldElement(18, 19)
        fe_6_19 = FieldElement(6, 19)
        fe_1_13 = FieldElement(1, 13)
        self.assertEqual(fe_7_19 + fe_11_19, fe_18_19)
        self.assertEqual(fe_7_19 + fe_12_19, fe_0_19)
        self.assertEqual(fe_7_19 + fe_18_19, fe_6_19)
        self.assertEqual(fe_7_19 + fe_0_19, fe_7_19)
        self.assertFalse(fe_7_19 - fe_0_19 == fe_11_19)
        with self.assertRaises(TypeError):
            fe_7_19 + fe_1_13

    def test_sub(self):
        fe_11_19 = FieldElement(11, 19)
        fe_9_19 = FieldElement(9, 19)
        fe_6_19 = FieldElement(6, 19)
        fe_0_19 = FieldElement(0, 19)
        fe_2_19 = FieldElement(2, 19)
        fe_12_19 = FieldElement(12, 19)
        fe_13_19 = FieldElement(13, 19)
        fe_1_13 = FieldElement(1, 13)
        self.assertEqual(fe_11_19 - fe_9_19, fe_2_19)
        self.assertEqual(fe_6_19 - fe_13_19, fe_12_19)
        self.assertEqual(fe_11_19 - fe_0_19, fe_11_19)
        self.assertFalse(fe_11_19 - fe_0_19 == fe_9_19)
        with self.assertRaises(TypeError):
            fe_11_19 - fe_1_13

    def test_mul(self):
        fe_5_19 = FieldElement(5, 19)
        fe_8_19 = FieldElement(8, 19)
        fe_17_19 = FieldElement(17, 19)
        fe_0_19 = FieldElement(0, 19)
        fe_1_19 = FieldElement(1, 19)
        fe_3_19 = FieldElement(3, 19)
        fe_15_19 = FieldElement(15, 19)
        fe_1_13 = FieldElement(1, 13)
        self.assertEqual(fe_5_19 * fe_3_19, fe_15_19)
        self.assertEqual(fe_8_19 * fe_17_19, fe_3_19)
        self.assertEqual(fe_5_19 * fe_0_19, fe_0_19)
        self.assertEqual(fe_5_19 * fe_1_19, fe_5_19)
        self.assertFalse(fe_5_19 * fe_0_19 == fe_8_19)
        with self.assertRaises(TypeError):
            fe_5_19 * fe_1_13

    def test_pow(self):
        fe_7_19 = FieldElement(7, 19)
        fe_9_19 = FieldElement(9, 19)
        fe_1_19 = FieldElement(1, 19)
        fe_0_19 = FieldElement(0, 19)
        fe_8_13 = FieldElement(8, 13)
        fe_7_13 = FieldElement(7, 13)
        self.assertEqual(fe_7_19 ** 3, fe_1_19)
        self.assertEqual(fe_9_19 ** 12, fe_7_19)
        self.assertFalse(fe_7_19 ** 1 == fe_0_19)
        self.assertEqual(fe_7_19 ** 0, fe_1_19)
        self.assertEqual(fe_9_19 ** 1, fe_9_19)
        self.assertEqual(fe_7_13 ** -3, fe_8_13)

    def test_true_div(self):
        fe_7_19 = FieldElement(7, 19)
        fe_5_19 = FieldElement(5, 19)
        fe_2_19 = FieldElement(2, 19)
        fe_1_19 = FieldElement(1, 19)
        fe_10_11 = FieldElement(10, 11)
        fe_0_19 = FieldElement(0, 19)
        fe_9_19 = FieldElement(9, 19)
        fe_3_19 = FieldElement(3, 19)
        self.assertEqual(fe_7_19 / fe_5_19, fe_9_19)
        self.assertEqual(fe_2_19 / fe_7_19, fe_3_19)
        self.assertEqual(fe_7_19 / fe_1_19, fe_7_19)
        self.assertFalse(fe_7_19 / fe_1_19 == fe_2_19)
        with self.assertRaises(TypeError):
            fe_7_19 / fe_10_11
        with self.assertRaises(ZeroDivisionError):
            fe_7_19 / fe_0_19


class PointTest(TestCase):
    def test_initialize(self):
        p1 = Point(-1, -1, 5, 7)
        p2 = Point(None, None, 5, 7)
        with self.assertRaises(ValueError):
            p3 = Point(-1, -2, 5, 7)

    def test_eq(self):
        p1 = Point(-1, -1, 5, 7)
        p2 = Point(-1, -1, 5, 7)
        p3 = Point(2, 5, 5, 7)
        self.assertEqual(p1, p2)
        self.assertFalse(p1 == p3)

    def test_ne(self):
        p1 = Point(-1, -1, 5, 7)
        p2 = Point(-1, -1, 5, 7)
        p3 = Point(2, 5, 5, 7)
        self.assertTrue(p1 != p3)
        self.assertFalse(p1 != p2)

    def test_add(self):
        p1 = Point(-1, -1, 5, 7)
        p2 = Point(None, None, 5, 7)
        p3 = Point(None, None, 0, 7)
        p4 = Point(-1, 1, 5, 7)
        p5 = Point(2, 5, 5, 7)
        p6 = Point(3, -7, 5, 7)
        p7 = Point(18, 77, 5, 7)
        p8 = Point(3, 0, 0, -27)
        p9 = Point(None, None, 0, -27)
        self.assertEqual(p1 + p2, p1)
        self.assertEqual(p1 + p4, p2)
        self.assertEqual(p5 + p1, p6)
        self.assertEqual(p1 + p1, p7)
        self.assertEqual(p8 + p8, p9)
        with self.assertRaises(TypeError):
            p1 + p3

    def on_curve_test(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        valid_points = ((192, 105), (17, 56), (1, 193))
        invalid_points = ((200, 119), (42, 99))
        for x_raw, y_raw in valid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            Point(x, y, a, b)
        for x_raw, y_raw in invalid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            with self.assertRaises(ValueError):
                Point(x, y, a, b)

    def test_add_over_finite_fields(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        # First assert
        x1 = FieldElement(170, prime)
        y1 = FieldElement(142, prime)
        p1 = Point(x1, y1, a, b)
        x2 = FieldElement(60, prime)
        y2 = FieldElement(139, prime)
        p2 = Point(x2, y2, a, b)
        x3 = FieldElement(220, prime)
        y3 = FieldElement(181, prime)
        p3 = Point(x3, y3, a, b)
        self.assertEqual(p1 + p2, p3)

        # Second assert
        x1 = FieldElement(47, prime)
        y1 = FieldElement(71, prime)
        p1 = Point(x1, y1, a, b)
        x2 = FieldElement(17, prime)
        y2 = FieldElement(56, prime)
        p2 = Point(x2, y2, a, b)
        x3 = FieldElement(215, prime)
        y3 = FieldElement(68, prime)
        p3 = Point(x3, y3, a, b)
        self.assertEqual(p1 + p2, p3)

        # Third assert
        x1 = FieldElement(143, prime)
        y1 = FieldElement(98, prime)
        p1 = Point(x1, y1, a, b)
        x2 = FieldElement(76, prime)
        y2 = FieldElement(66, prime)
        p2 = Point(x2, y2, a, b)
        x3 = FieldElement(47, prime)
        y3 = FieldElement(71, prime)
        p3 = Point(x3, y3, a, b)
        self.assertEqual(p1 + p2, p3)

    def test_rmul(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x1 = FieldElement(47, prime)
        y1 = FieldElement(71, prime)
        p1 = Point(x1, y1, a, b)
        x2 = FieldElement(36, prime)
        y2 = FieldElement(111, prime)
        p2 = Point(x2, y2, a, b)
        x3 = FieldElement(15, prime)
        y3 = FieldElement(86, prime)
        p3 = Point(x3, y3, a, b)
        p4 = Point(None, None, a, b)
        self.assertEqual(2 * p1, p2)
        self.assertEqual(1 * p1, p1)
        self.assertEqual(18 * p1, p3)
        self.assertEqual(21 * p1, p4)


class S256PointTest(TestCase):
    def test_order(self):
        g = S256Point(Gx, Gy)
        p = N * g
        p_inf = S256Point(None, None)
        self.assertEqual(p, p_inf)

    def test_verify_signature(self):
        p = S256Point(0x887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c,
                      0x61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34)

        z1 = 0xec208baa0fc1c19f708a9ca96fdeff3ac3f230bb4a7ba4aede4942ad003c0f60
        r1 = 0xac8d1c87e51d0d441be8b3dd5b05c8795b48875dffe00b7ffcfac23010d3a395
        s1 = 0x68342ceff8935ededd102dd876ffd6ba72d6a427a3edb13d26eb0781cb423c4
        sig1 = Signature(r1, s1)
        self.assertTrue(p.verify(z1, sig1))

        z2 = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
        r2 = 0xeff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c
        s2 = 0xc7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6
        sig2 = Signature(r2, s2)
        self.assertTrue(p.verify(z2, sig2))

        self.assertFalse(p.verify(z1, sig2))

    def test_sec(self):
        g = S256Point(Gx, Gy)
        px = 0x887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c
        py = 0x61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34
        p = S256Point(px, py)
        self.assertEqual(g.sec(False), b'\x04' + Gx.to_bytes(32, 'big') + Gy.to_bytes(32, 'big'))
        self.assertEqual(p.sec(False), b'\x04' + px.to_bytes(32, 'big') + py.to_bytes(32, 'big'))
        self.assertFalse(p.sec(False) == b'\x04' + Gx.to_bytes(32, 'big') + Gy.to_bytes(32, 'big'))
        self.assertEqual(p.sec(), b'\x02' + px.to_bytes(32, 'big'))
        self.assertEqual(g.sec(), b'\x02' + Gx.to_bytes(32, 'big'))
        self.assertFalse(p.sec() == b'\x03' + px.to_bytes(32, 'big'))


class SignatureTest(TestCase):
    def test_der(self):
        r1 = 0xac8d1c87e51d0d441be8b3dd5b05c8795b48875dffe00b7ffcfac23010d3a395
        s1 = 0x68342ceff8935ededd102dd876ffd6ba72d6a427a3edb13d26eb0781cb423c4
        sig1 = Signature(r1, s1)

        r2 = 0xeff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c
        s2 = 0xc7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6
        sig2 = Signature(r2, s2)

        der_sig_1 = (b'\x30' + b'\x45' + b'\x02' + b'\x21' + b'\x00'
                     + r1.to_bytes(32, 'big') + b'\x02' + b'\x20' + s1.to_bytes(32, 'big'))
        self.assertEqual(sig1.der(), der_sig_1)

        def_sig_2 = (b'\x30' + b'\x45' + b'\x02' + b'\x20' + b'\x00'
                     + r2.to_bytes(32, 'big').lstrip(b'\x00') + b'\x02' + b'\x21' + b'\x00' + s2.to_bytes(32, 'big'))
        self.assertEqual(sig2.der(), def_sig_2)


class PrivateKey(TestCase):
    def test_address(self):
        self.skipTest('Weird behavior')
        p1 = PrivateKey(5002)
        a1 = p1.point.address(False, True)
        a2 = 'mmTPbXQFxboEtNRkwfh6K51jvdtHLxGeMA'
        self.assertEqual(a1, a2)

        p2 = PrivateKey(2020 ** 5)
        a3 = p2.point.address(True, True)
        a4 = 'mopVkxp8UhXqRYbCYJsbeE1h1fiF64jcoH'
        self.assertEqual(a3, a4)

        p3 = PrivateKey(0x12345deadbeef)
        a5 = p3.point.address(True, False)
        a6 = '1F1Pn2y6pDb68E5nYJJeba4TLg2U7B6KF1'
        self.assertEqual(a5, a6)
        self.assertFalse(a1 == a6)

    def test_wif(self):
        self.skipTest('Weird behavior')
        p1 = PrivateKey(5003)
        w1 = p1.wif(True, True)
        w2 = 'cMahea7zqjxrtgAbB7LSGbcQUr1uX1ojuat9jZodMN8rFTv2sfUK'
        self.assertEqual(w1, w2)

        p2 = PrivateKey(2021 ** 5)
        w3 = p2.wif(False, True)
        w4 = '91avARGdfge8E4tZfYLoxeJ5sGBdNJQH4kvjpWAxgzczjbCwxic'
        self.assertEqual(w3, w4)

        p3 = PrivateKey(0x54321deadbeef)
        w5 = p3.wif()
        w6 = 'KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgiuQJv1h8Ytr2S53a'
        self.assertEqual(w5, w6)
        self.assertFalse(w1 == w6)
