import unittest
from src.logic_expression import LogicExpressions
from src.calculation_minimizer import CalculationMinimizer
from src.tabular_minimizer import TabularMinimizer
from src.karnaugh_minimizer import KarnaughMinimizer
from src.boolean_function import BooleanFunction
from copy import deepcopy

class TestMinimizers(unittest.TestCase):
    def setUp(self):
        # Создаём неизменяемую копию тестовых данных
        self.test_cases = [
            {
                "expression": "(a ∧ b ∧ ¬c) ∨ (¬a ∧ b ∧ d) ∨ (a ∧ ¬b ∧ c ∧ ¬d)",
                "dnf_result": {"ab¬c", "a¬bc¬d", "¬abd"},
                "cnf_result": {"(a∨d)", "(¬a∨¬b∨¬c)", "(b∨¬d)", "(b∨c)"}
            },
            {
                "expression": "(¬a ∧ b ∧ c) ∨ (a ∧ ¬b ∧ ¬c) ∨ (a ∧ ¬b ∧ c) ∨ (a ∧ b ∧ ¬c) ∨ (a ∧ b ∧ c)",
                "dnf_result": {"a", "bc"},
                "cnf_result": {"(a∨b)", "(a∨c)"}
            }
        ]
        # Делаем глубокую копию, чтобы предотвратить изменения
        self.test_cases = deepcopy(self.test_cases)
        self.minimizers = [
            ("CalculationMinimizer", CalculationMinimizer),
            ("TabularMinimizer", TabularMinimizer),
            ("KarnaughMinimizer", KarnaughMinimizer)
        ]

    def _split_result(self, result, is_dnf):
        if not isinstance(result, str):
            raise ValueError(f"Ожидалась строка, получен ")
        if is_dnf:
            return set(term.replace("∧", "") for term in result.split(" ∨ "))
        else:
            return set(term.strip() for term in result.split(" ∧ "))

    def test_minimizers_dnf(self):
        for case in self.test_cases:
            logic = LogicExpressions(case["expression"])
            sdnf, _ = logic.build_sdnf()
            sdnf_terms = sorted([term.strip('()') for term in sdnf.split(' ∨ ')])
            sdnf_func = BooleanFunction(sdnf_terms, is_dnf=True)
            print(f"\n=== DNF Test: {case['expression']} ===")
            print(f"SDNF terms: {sdnf_terms}")
            print(f"Expected DNF: {case['dnf_result']}")

            for name, MinimizerClass in self.minimizers:
                minimizer = MinimizerClass(sdnf_func)
                result = minimizer.minimize()["result"]
                result_set = self._split_result(result, is_dnf=True)
                print(f"{name} result: {result_set}")
                self.assertEqual(result_set, case["dnf_result"],
                                 f"Failed DNF for {name} with expression {case['expression']}")

    def test_minimizers_cnf(self):
        for case in self.test_cases:
            logic = LogicExpressions(case["expression"])
            sknf, _ = logic.build_sknf()
            sknf_terms = sorted([term.strip('()') for term in sknf.split(' ∧ ')])
            sknf_func = BooleanFunction(sknf_terms, is_dnf=False)
            print(f"\n=== CNF Test: {case['expression']} ===")
            print(f"SKNF terms: {sknf_terms}")
            print(f"Expected CNF (from setUp): {case['cnf_result']}")

            for name, MinimizerClass in self.minimizers:
                minimizer = MinimizerClass(sknf_func)
                result = minimizer.minimize()["result"]
                result_set = self._split_result(result, is_dnf=False)
                print(f"{name} result: {result_set}")
                # Дополнительная проверка перед сравнением
                print(f"Comparing with expected: {case['cnf_result']}")
                self.assertEqual(result_set, case["cnf_result"],
                                 f"Failed CNF for {name} with expression {case['expression']}")

if __name__ == "__main__":
    unittest.main()