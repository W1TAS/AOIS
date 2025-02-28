import unittest
from lab1.classes.BinaryOperations import BinaryOperations
class TestBinaryOperations(unittest.TestCase):

    def test_int_to_direct_code(self):
        self.assertEqual(BinaryOperations.int_to_direct_code(5), '0000000000000101')  # 16 бит
        self.assertEqual(BinaryOperations.int_to_direct_code(-5), '1000000000000101')  # 16 бит

    def test_int_to_inverted_code(self):
        self.assertEqual(BinaryOperations.int_to_inverted_code(5), '0000000000000101')  # 16 бит
        self.assertEqual(BinaryOperations.int_to_inverted_code(-5), '1111111111111010')  # 16 бит

    def test_int_to_additional_code(self):
        self.assertEqual(BinaryOperations.int_to_additional_code(5), '0000000000000101')  # 16 бит
        self.assertEqual(BinaryOperations.int_to_additional_code(-5), '1111111111111011')  # 16 бит

    def test_direct_to_decimal(self):
        self.assertEqual(BinaryOperations.direct_to_decimal('0000000000000101'), 5)  # 16 бит
        self.assertEqual(BinaryOperations.direct_to_decimal('1000000000000101'), -5)  # 16 бит

    def test_additional_to_decimal(self):
        self.assertEqual(BinaryOperations.additional_to_decimal('0000000000000101'), 5)  # 16 бит
        self.assertEqual(BinaryOperations.additional_to_decimal('1111111111111011'), -5)  # 16 бит

    def test_add_additional(self):
        self.assertEqual(BinaryOperations.add_additional('0000000000000101', '0000000000000101'), '0000000000001010')  # 16 бит
        self.assertEqual(BinaryOperations.add_additional('1111111111111011', '0000000000000101'), '0000000000000000')  # 16 бит

    def test_binary_subtraction(self):
        self.assertEqual(BinaryOperations.binary_subtraction('0000000000001010', '0000000000000101'), '0000000000000101')  # 16 бит
        self.assertEqual(BinaryOperations.binary_subtraction('0000000000000000', '0000000000000101'), '1111111111111011')  # 16 бит

    def test_binary_multiplication(self):
        self.assertEqual(BinaryOperations.binary_multiplication('0000000000000101', '0000000000000101'), '0000000000011001')  # 16 бит
        self.assertEqual(BinaryOperations.binary_multiplication('1000000000000101', '0000000000000111'), '1000000000100011')

    def test_binary_division(self):
        self.assertEqual(BinaryOperations.binary_division('1000000000001110', '0000000000011100'), '1000000000000000.10000')  # 16 бит
        self.assertEqual(BinaryOperations.binary_division('1000000000001110', '1000000000011100'), '0000000000000000.10000')  # 16 бит

    def test_bin_frac_to_dec_frac(self):
        self.assertEqual(BinaryOperations.bin_frac_to_dec_frac('1000000000000000.10000'), -0.5)  # 16 бит
        self.assertEqual(BinaryOperations.bin_frac_to_dec_frac('0000000000001010.1000'), 10.5)  # 16 бит

if __name__ == '__main__':
    unittest.main()
