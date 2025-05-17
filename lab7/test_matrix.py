import unittest
import random
from src.matrix import Matrix

class TestMatrix(unittest.TestCase):
    def setUp(self):
        """Set up a Matrix instance for each test."""
        random.seed(42)  # Ensure reproducible random results
        self.matrix = Matrix(size=16)

    def test_init(self):
        """Test matrix initialization."""
        self.assertEqual(self.matrix.size, 16)
        self.assertEqual(len(self.matrix.matrix), 16)
        self.assertEqual(len(self.matrix.matrix[0]), 16)
        self.assertEqual(len(self.matrix.g), 16)
        self.assertEqual(len(self.matrix.g[0]), 17)
        self.assertEqual(len(self.matrix.l), 16)
        self.assertEqual(len(self.matrix.l[0]), 17)
        # Check that matrix contains only 0s and 1s
        for row in self.matrix.matrix:
            for bit in row:
                self.assertIn(bit, [0, 1])

    def test_get_word(self):
        """Test getting a word (column) with diagonal addressing."""
        word = self.matrix.get_word(0)
        self.assertEqual(len(word), 16)
        # Verify diagonal addressing
        for i in range(16):
            row = (i + 0) % 16
            self.assertEqual(word[i], self.matrix.matrix[row][0])

    def test_set_word(self):
        """Test setting a word (column) with diagonal addressing."""
        new_word = [1] * 16
        self.matrix.set_word(0, new_word)
        retrieved_word = self.matrix.get_word(0)
        self.assertEqual(retrieved_word, new_word)
        # Verify matrix was updated correctly
        for i in range(16):
            row = (i + 0) % 16
            self.assertEqual(self.matrix.matrix[row][0], 1)

    def test_display_word_valid(self):
        """Test displaying a valid word."""
        result = self.matrix.display_word(0)
        self.assertTrue(result.startswith("Слово 0: "))
        word = self.matrix.get_word(0)
        expected = f"Слово 0: {''.join(str(bit) for bit in word)}"
        self.assertEqual(result, expected)

    def test_display_word_invalid(self):
        """Test displaying a word with invalid column index."""
        result = self.matrix.display_word(16)
        self.assertEqual(result, "Ошибка: столбец 16 вне диапазона (0..15)")

    def test_compute_gl(self):
        """Test compute_gl method."""
        argument = 0b1010101010101010  # Example argument
        self.matrix.compute_gl(argument)
        for j in range(self.matrix.size):
            # Check that g and l arrays are filled with 0s and 1s
            for i in range(self.matrix.size + 1):
                self.assertIn(self.matrix.g[j][i], [0, 1])
                self.assertIn(self.matrix.l[j][i], [0, 1])

    def test_search_by_match(self):
        """Test search_by_match method."""
        argument = 0b1111000011110000
        columns, max_matches = self.matrix.search_by_match(argument)
        self.assertTrue(isinstance(columns, list))
        self.assertTrue(isinstance(max_matches, int))
        self.assertTrue(0 <= max_matches <= 16)
        # Verify that returned columns have the maximum number of matches
        for j in columns:
            word = self.matrix.get_word(j)
            matches = sum(1 for i in range(16) if word[i] == ((argument >> i) & 1))
            self.assertEqual(matches, max_matches)

    def test_logical_operation_valid(self):
        """Test logical_operation with valid function IDs."""
        # Test f5 (copy word2 to target)
        self.matrix.set_word(1, [1] * 16)
        self.matrix.set_word(2, [0] * 16)
        result = self.matrix.logical_operation(5, 1, 2, 3)
        self.assertEqual(result, "Операция f5 выполнена: столбцы 1 и 2 -> столбец 3")
        self.assertEqual(self.matrix.get_word(3), [0] * 16)

        # Test f0 (all zeros)
        result = self.matrix.logical_operation(0, 1, 2, 3)
        self.assertEqual(result, "Операция f0 выполнена: столбцы 1 и 2 -> столбец 3")
        self.assertEqual(self.matrix.get_word(3), [0] * 16)

        # Test f15 (all Ones)
        result = self.matrix.logical_operation(15, 1, 2, 3)
        self.assertEqual(result, "Операция f15 выполнена: столбцы 1 и 2 -> столбец 3")
        self.assertEqual(self.matrix.get_word(3), [1] * 16)

    def test_logical_operation_invalid(self):
        """Test logical_operation with invalid inputs."""
        # Invalid function ID
        result = self.matrix.logical_operation(7, 0, 1, 2)
        self.assertEqual(result, "Ошибка: функция f7 не поддерживается (доступны f0, f5, f10, f15)")

        # Invalid column index
        result = self.matrix.logical_operation(5, 16, 1, 2)
        self.assertEqual(result, "Ошибка: столбцы 16, 1, 2 должны быть в диапазоне 0..15")

    def test_extract_bits(self):
        """Test extract_bits method."""
        word = [0, 1, 1, 0, 1] + [0] * 11  # Example word: 01101...
        value = self.matrix.extract_bits(word, 0, 4)
        self.assertEqual(value, 0b01101)  # Binary 01101 = 13

    def test_set_bits(self):
        """Test set_bits method."""
        word = [0] * 16
        value = 0b101  # Binary 101 = 5
        updated_word = self.matrix.set_bits(word, 0, 2, value)
        expected = [1, 0, 1] + [0] * 13
        self.assertEqual(updated_word, expected)

    def test_add_fields(self):
        """Test add_fields method."""
        # Set up a word with V=0b101, A=0b0011, B=0b0101
        word = [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1] + [0] * 5
        self.matrix.set_word(0, word)
        results = self.matrix.add_fields(V_key=0b101)
        self.assertTrue(len(results) >= 1)
        for col, sum_AB, word_str in results:
            self.assertEqual(col, 0)
            self.assertEqual(sum_AB, (0b0011 + 0b0101) & 0b11111)  # 3 + 5 = 8
            # Verify last 5 bits of word are sum_AB
            retrieved_word = self.matrix.get_word(col)
            last_5_bits = self.matrix.extract_bits(retrieved_word, 11, 15)
            self.assertEqual(last_5_bits, sum_AB)

if __name__ == '__main__':
    unittest.main()