import unittest
from LogicExpression import LogicExpressions

class TestLogicExpressions(unittest.TestCase):
    def test_truth_table(self):
        logic = LogicExpressions("A & B")
        expected_table = [
            ((0, 0), 0),
            ((0, 1), 0),
            ((1, 0), 0),
            ((1, 1), 1)
        ]
        self.assertEqual(logic.table, expected_table)

    def test_sdnf(self):
        logic = LogicExpressions("A | B")
        sdnf, indices = logic.build_sdnf()
        self.assertEqual(sdnf, "(¬A∧B) ∨ (A∧¬B) ∨ (A∧B)")
        self.assertEqual(indices, "(1, 2, 3)")

    def test_sknf(self):
        logic = LogicExpressions("A & B")
        sknf, indices = logic.build_sknf()
        self.assertEqual(sknf, "(A∨B) ∧ (A∨¬B) ∧ (¬A∨B)")
        self.assertEqual(indices, "(0, 1, 2)")

    def test_index_form(self):
        logic = LogicExpressions("A -> B")
        self.assertEqual(logic.calculate_index_form(), "13 - 1101")

    def test_complex_expression(self):
        logic = LogicExpressions("(A∨B)∧((!C)→D)")
        expected_table = [
            ((0, 0, 0, 0), 0),
            ((0, 0, 0, 1), 0),
            ((0, 0, 1, 0), 0),
            ((0, 0, 1, 1), 0),
            ((0, 1, 0, 0), 0),
            ((0, 1, 0, 1), 1),
            ((0, 1, 1, 0), 1),
            ((0, 1, 1, 1), 1),
            ((1, 0, 0, 0), 0),
            ((1, 0, 0, 1), 1),
            ((1, 0, 1, 0), 1),
            ((1, 0, 1, 1), 1),
            ((1, 1, 0, 0), 0),
            ((1, 1, 0, 1), 1),
            ((1, 1, 1, 0), 1),
            ((1, 1, 1, 1), 1)
        ]
        self.assertEqual(logic.table, expected_table)

    def test_all_operations(self):
        logic = LogicExpressions("¬A ∧ B ∨ (A → B) ↔ (A ∨ ¬B)")
        expected_table = [
            ((0, 0), 1),
            ((0, 1), 0),
            ((1, 0), 0),
            ((1, 1), 1)
        ]
        self.assertEqual(logic.table, expected_table)

    def test_print_truth_table(self):
        logic = LogicExpressions("A & B")
        expected_output = "\nТаблица истинности:\nA | B | Result\n--------------\n0 | 0 | 0\n0 | 1 | 0\n1 | 0 | 0\n1 | 1 | 1\n"
        from io import StringIO
        import sys
        captured_output = StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output
        try:
            logic.print_truth_table()
        finally:
            sys.stdout = original_stdout
        self.assertEqual(captured_output.getvalue(), expected_output)

