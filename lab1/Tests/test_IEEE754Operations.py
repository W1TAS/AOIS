import unittest
from lab1.classes.IEEE754Operations import IEEE754Operations

class TestIEEE754Operations(unittest.TestCase):

    def test_binary_to_decimal(self):
        self.assertEqual(IEEE754Operations.binary_to_decimal('00000001'), 1)
        self.assertEqual(IEEE754Operations.binary_to_decimal('00000010'), 2)
        self.assertEqual(IEEE754Operations.binary_to_decimal('11111111'), 255)

    def test_float_to_ieee754(self):
        self.assertEqual(IEEE754Operations.float_to_ieee754(0.0), '0'*32)
        self.assertEqual(IEEE754Operations.float_to_ieee754(1.0), '00111111100000000000000000000000')
        self.assertEqual(IEEE754Operations.float_to_ieee754(-1.0), '10111111100000000000000000000000')

    def test_ieee754_to_float(self):
        self.assertAlmostEqual(IEEE754Operations.ieee754_to_float('00111111100000000000000000000000'), 1.0)
        self.assertAlmostEqual(IEEE754Operations.ieee754_to_float('10111111100000000000000000000000'), -1.0)

    def test_ieee754_to_binary_exp(self):
        mantissa, exponent = IEEE754Operations.ieee754_to_binary_exp('00111111100000000000000000000000')
        self.assertEqual(mantissa, '100000000000000000000000')
        self.assertEqual(exponent, 0)

    def test_add_ieee754_0(self):

        result = IEEE754Operations.add_ieee754('100000000000000000000000', -127, '100000000000000000000000', -127)
        self.assertEqual(result, '0'*32)

    def test_add_ieee754(self):
        x_m, x_e = IEEE754Operations.ieee754_to_binary_exp('00111110000000000000000000000000')
        y_m, y_e = IEEE754Operations.ieee754_to_binary_exp('01000010111101100010000000000000')
        result1 = IEEE754Operations.add_ieee754(x_m, x_e, y_m, y_e)
        result2 = IEEE754Operations.add_ieee754(y_m, y_e, x_m, x_e)
        self.assertEqual(result1, "01000010111101100110000000000000")
        self.assertEqual(result2, "01000010111101100110000000000000")


    def test_to_binary(self):
        self.assertEqual(IEEE754Operations.to_binary(5), '101')
        self.assertEqual(IEEE754Operations.to_binary(255), '11111111')

if __name__ == '__main__':
    unittest.main()
