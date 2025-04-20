from src.calculation_minimizer import CalculationMinimizer
from src.tabular_minimizer import TabularMinimizer
from src.karnaugh_minimizer import KarnaughMinimizer
from src.boolean_function import BooleanFunction
import unittest


class TestMinimizer(unittest.TestCase):
    def setUp(self):
        self.expressions = [
            "a∨¬b∧c",
            "¬a∧b∨¬c∧d",
            "a∧b∨¬c∧¬d∨e",
            # "a∧¬b∧c∨¬d∧e",
            "¬a∨b∧¬c∨d"
        ]
        # Тестовые выражения (убраны выражения с 5 переменными)

    def parse_expression(self, expr, is_dnf):
        """
        Парсит строку выражения в список термов.
        Для ДНФ разделяет по ∨, для КНФ — по ∧.
        """
        terms = []
        current_term = ""
        i = 0
        while i < len(expr):
            if is_dnf and expr[i] == "∨":
                if current_term:
                    terms.append(current_term)
                    current_term = ""
                i += 1
            elif not is_dnf and expr[i] == "∧":
                if current_term:
                    terms.append(current_term)
                    current_term = ""
                i += 1
            else:
                current_term += expr[i]
                i += 1
        if current_term:
            terms.append(current_term)
        return terms

    def normalize_result(self, result):
        # Удаляем пробелы
        result = result.replace(" ", "")

        # Для ДНФ: ожидаем термы, разделённые ∨
        if "∨" in result and "∧" not in result.replace("¬", ""):
            # Убираем лишние ∨∨
            while "∨∨" in result:
                result = result.replace("∨∨", "∨")
            terms = result.split("∨")
            terms = [term for term in terms if term]  # Убираем пустые термы
            terms.sort()
            return "∨".join(terms)
        # Для КНФ: ожидаем термы в скобках, разделённые ∧
        elif "∧" in result:
            terms = result.split("∧")
            normalized_terms = []
            for term in terms:
                term = term.strip("()")
                # Убираем лишние ∨∨ внутри терма
                while "∨∨" in term:
                    term = term.replace("∨∨", "∨")
                literals = []
                i = 0
                while i < len(term):
                    if term[i] == "¬":
                        literals.append(term[i:i + 2])
                        i += 2
                    else:
                        literals.append(term[i])
                        i += 1
                literals = [lit for lit in literals if lit]  # Убираем пустые литералы
                literals.sort()
                normalized_terms.append(f"({'∨'.join(literals)})")
            normalized_terms.sort()
            return "∧".join(normalized_terms)
        return result

    def test_minimization_dnf(self):
        for expr in self.expressions:
            with self.subTest(expr=expr):
                # Парсим выражение для ДНФ
                terms = self.parse_expression(expr, is_dnf=True)
                # Создаём объект BooleanFunction для ДНФ
                bf_dnf = BooleanFunction(terms, is_dnf=True)

                # Минимизация с помощью трёх методов
                calc_minimizer = CalculationMinimizer(bf_dnf)
                tabular_minimizer = TabularMinimizer(bf_dnf)
                karnaugh_minimizer = KarnaughMinimizer(bf_dnf)

                calc_result = calc_minimizer.minimize()['result']
                tabular_result = tabular_minimizer.minimize()['result']
                karnaugh_result = karnaugh_minimizer.minimize()['result']

                # Нормализуем результаты для сравнения
                calc_result = self.normalize_result(calc_result)
                tabular_result = self.normalize_result(tabular_result)
                karnaugh_result = self.normalize_result(karnaugh_result)

                # Сравниваем результаты
                self.assertEqual(calc_result, tabular_result,
                                 f"ДНФ: Calculation и Tabular дают разные результаты для {expr}")
                self.assertEqual(calc_result, karnaugh_result,
                                 f"ДНФ: Calculation и Karnaugh дают разные результаты для {expr}")

    def test_minimization_cnf(self):
        for expr in self.expressions:
            with self.subTest(expr=expr):
                # Парсим выражение для КНФ
                terms = self.parse_expression(expr, is_dnf=False)
                # Создаём объект BooleanFunction для КНФ
                bf_cnf = BooleanFunction(terms, is_dnf=False)

                # Минимизация с помощью трёх методов
                calc_minimizer = CalculationMinimizer(bf_cnf)
                tabular_minimizer = TabularMinimizer(bf_cnf)
                karnaugh_minimizer = KarnaughMinimizer(bf_cnf)

                calc_result = calc_minimizer.minimize()['result']
                tabular_result = tabular_minimizer.minimize()['result']
                karnaugh_result = karnaugh_minimizer.minimize()['result']

                # Нормализуем результаты для сравнения
                calc_result = self.normalize_result(calc_result)
                tabular_result = self.normalize_result(tabular_result)
                karnaugh_result = self.normalize_result(karnaugh_result)

                # Сравниваем результаты
                self.assertEqual(calc_result, tabular_result,
                                 f"КНФ: Calculation и Tabular дают разные результаты для {expr}")
                self.assertEqual(calc_result, karnaugh_result,
                                 f"КНФ: Calculation и Karnaugh дают разные результаты для {expr}")


if __name__ == '__main__':
    unittest.main()