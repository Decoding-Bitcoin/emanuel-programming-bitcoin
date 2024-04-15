from unittest import TestCase
from pybtc.ecc import FieldElement


class FieldElementTest(TestCase):
    def test_eq(self):
        a = FieldElement(10, 13)
        b = FieldElement(10, 13)
        c = FieldElement(6, 13)
        d = FieldElement(6, 11)
        self.assertEqual(a, b)
        self.assertFalse(a == c)

    def test_ne(self):
        a = FieldElement(10, 13)
        b = FieldElement(10, 13)
        c = FieldElement(6, 13)
        d = FieldElement(6, 11)
        self.assertTrue(a != c)
        self.assertFalse(a != b)

    def test_add(self):
        a = FieldElement(7, 19)
        b = FieldElement(11, 19)
        c = FieldElement(12, 19)
        d = FieldElement(0, 19)
        e = FieldElement(18, 19)
        f = FieldElement(6, 19)
        g = FieldElement(1, 13)
        self.assertEqual(a + b, e)
        self.assertEqual(a + c, d)
        self.assertEqual(a + e, f)
        self.assertEqual(a + d, a)
        with self.assertRaises(TypeError):
            a + g

    def test_sub(self):
        a = FieldElement(11, 19)
        b = FieldElement(9, 19)
        c = FieldElement(6, 19)
        d = FieldElement(0, 19)
        e = FieldElement(2, 19)
        f = FieldElement(12, 19)
        g = FieldElement(13, 19)
        h = FieldElement(1, 13)
        self.assertEqual(a - b, e)
        self.assertEqual(c - g, f)
        self.assertEqual(a - d, a)
        with self.assertRaises(TypeError):
            a - h

    def test_mul(self):
        a = FieldElement(5, 19)
        b = FieldElement(8, 19)
        c = FieldElement(17, 19)
        d = FieldElement(0, 19)
        e = FieldElement(1, 19)
        f = FieldElement(3, 19)
        g = FieldElement(15, 19)
        h = FieldElement(1, 13)
        self.assertEqual(a * f, g)
        self.assertEqual(b * c, f)
        self.assertEqual(a * d, d)
        self.assertEqual(a * e, a)
        with self.assertRaises(TypeError):
            a * h
