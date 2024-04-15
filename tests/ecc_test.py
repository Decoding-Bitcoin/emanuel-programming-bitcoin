from unittest import TestCase
from pybtc.ecc import FieldElement


class FieldElementTest(TestCase):
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
