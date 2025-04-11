import unittest
from src.logic_expression import LogicExpressions
from src.calculation_minimizer import CalculationMinimizer
from src.tabular_minimizer import TabularMinimizer
from src.karnaugh_minimizer import KarnaughMinimizer
from src.boolean_function import BooleanFunction


class TestMinimizers(unittest.TestCase):
    def setUp(self):
        # Тестовые случаи: выражение и ожидаемые результаты для СДНФ и СКНФ как множества
        self.test_cases = [
            # Пример 1: (a ∧ b ∧ ¬c) ∨ (¬a ∧ b ∧ d) ∨ (a ∧ ¬b ∧ c ∧ ¬d)
            {
                "expression": "(a ∧ b ∧ ¬c) ∨ (¬a ∧ b ∧ d) ∨ (a ∧ ¬b ∧ c ∧ ¬d)",
                "dnf_result": {"ab¬c", "a¬bc¬d", "¬abd"},  # Без ∧
                "cnf_result": {"(a∨d)", "(b∨c)", "(¬a∨¬b∨¬c)", "(b∨¬d)"}
            },
            # Пример 2: (¬a ∧ b ∧ c) ∨ (a ∧ ¬b ∧ ¬c) ∨ (a ∧ b ∧ c)
            # {
            #     "expression": "(¬a ∧ b ∧ c) ∨ (a ∧ ¬b ∧ ¬c) ∨ (a ∧ b ∧ c)",
            #     "dnf_result": {"a¬b¬c", "bc"},  # Без ∧
            #     "cnf_result": {"(¬b∨c)", "(b∨¬c)", "(a∨c)"}
            #
            # }
            # Пример 3: (¬a ∧ b ∧ c) ∨ (a ∧ ¬b ∧ ¬c) ∨ (a ∧ ¬b ∧ c) ∨ (a ∧ b ∧ ¬c) ∨ (a ∧ b ∧ c)
            {
                "expression": "(¬a ∧ b ∧ c) ∨ (a ∧ ¬b ∧ ¬c) ∨ (a ∧ ¬b ∧ c) ∨ (a ∧ b ∧ ¬c) ∨ (a ∧ b ∧ c)",
                "dnf_result": {"a", "bc"},  # Без ∧
                "cnf_result": {"(a∨b)", "(a∨c)"}
            },
            # # Пример 4: (a ∧ b) ∨ (¬a ∧ ¬b ∧ c) ∨ (a ∧ ¬c ∧ d)
            # {
            #     "expression": "(a ∧ b) ∨ (¬a ∧ ¬b ∧ c) ∨ (a ∧ ¬c ∧ d)",
            #     "dnf_result": {"ab", "¬a¬bc", "a¬cd"},  # Без ∧
            #     "cnf_result": {"(a∨c)", "(b∨c∨d)", "(¬a∨b∨d)"}
            # }
        ]
        self.minimizers = [
            ("CalculationMinimizer", CalculationMinimizer),
            ("TabularMinimizer", TabularMinimizer),
            ("KarnaughMinimizer", KarnaughMinimizer)
        ]

    def _split_result(self, result, is_dnf):
        """Разбивает строковый результат на множество импликант, убирая ∧ для СДНФ."""
        if not isinstance(result, str):
            raise ValueError(f"Ожидалась строка, получен {type(result)}")

        if is_dnf:
            # Для СДНФ: разделяем по " ∨ " и убираем ∧
            return set(term.replace("∧", "") for term in result.split(" ∨ "))
        else:
            # Для СКНФ: разделяем по " ∧ ", оставляем скобки
            return set(term.strip() for term in result.split(" ∧ "))

    def test_minimizers_dnf(self):
        for case in self.test_cases:
            logic = LogicExpressions(case["expression"])
            sdnf, _ = logic.build_sdnf()
            sdnf_terms = [term.strip('()') for term in sdnf.split(' ∨ ')]
            sdnf_func = BooleanFunction(sdnf_terms, is_dnf=True)

            for name, MinimizerClass in self.minimizers:
                minimizer = MinimizerClass(sdnf_func)
                result = minimizer.minimize()["result"]
                result_set = self._split_result(result, is_dnf=True)
                self.assertEqual(result_set, case["dnf_result"],
                                 f"Failed DNF for {name} with expression {case['expression']}")

    def test_minimizers_cnf(self):
        for case in self.test_cases:
            logic = LogicExpressions(case["expression"])
            sknf, _ = logic.build_sknf()
            sknf_terms = [term.strip('()') for term in sknf.split(' ∧ ')]
            sknf_func = BooleanFunction(sknf_terms, is_dnf=False)
            print(sknf_func.terms)
            for name, MinimizerClass in self.minimizers:
                minimizer = MinimizerClass(sknf_func)
                result = minimizer.minimize()["result"]
                result_set = self._split_result(result, is_dnf=False)
                print(result_set)
                self.assertEqual(result_set, case["cnf_result"],
                                 f"Failed CNF for {name} with expression {case['expression']}")


if __name__ == "__main__":
    unittest.main()