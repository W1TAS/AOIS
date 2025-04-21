from src.boolean_function import BooleanFunction
from src.calculation_minimizer import CalculationMinimizer

# Таблица истинности для ОДС-3
truth_table_data = [
    (0, 0, 0, 0, 0),  # A, B, Cin, S, Cout
    (0, 0, 1, 1, 0),
    (0, 1, 0, 1, 0),
    (0, 1, 1, 0, 1),
    (1, 0, 0, 1, 0),
    (1, 0, 1, 0, 1),
    (1, 1, 0, 0, 1),
    (1, 1, 1, 1, 1)
]


def print_truth_table():
    """Выводит таблицу истинности для ОДС-3."""
    print("\nТаблица истинности для ОДС-3:")
    header = "A | B | Cin | S | Cout"
    print(header)
    print("-" * len(header))
    for row in truth_table_data:
        print(f"{row[0]} | {row[1]} |  {row[2]}  | {row[3]} |  {row[4]}")

def build_sknf_for_output(table, output_index, variables):
    """Строит СКНФ для указанного выхода."""
    terms = []
    for index, row in enumerate(table):
        if row[output_index] == 0:  # Для СКНФ берем строки, где выход = 0
            term = []
            for var, val in zip(variables, row[:3]):  # Берем только входы A, B, Cin
                term.append(f"{'¬' if val == 1 else ''}{var}")
            terms.append(f"({'∨'.join(term)})")
    return terms

def main():
    # Вывод таблицы истинности
    print_truth_table()

    # Переменные
    variables = ['A', 'B', 'C']  # Cin обозначим как C для краткости

    # Построение СКНФ для S (выход в столбце 3)
    s_terms = build_sknf_for_output(truth_table_data, 3, variables)
    s_sknf = BooleanFunction(s_terms, is_dnf=False)
    print("\nСКНФ для S:")
    print(s_sknf)

    # Минимизация СКНФ для S
    s_minimizer = CalculationMinimizer(s_sknf)
    s_minimized_result = s_minimizer.minimize()
    print("\nМинимизированная СКНФ для S:")
    print(s_minimized_result['result'])

    # Построение СКНФ для Cout (выход в столбце 4)
    cout_terms = build_sknf_for_output(truth_table_data, 4, variables)
    cout_sknf = BooleanFunction(cout_terms, is_dnf=False)
    print("\nСКНФ для Cout:")
    print(cout_sknf)

    # Минимизация СКНФ для Cout
    cout_minimizer = CalculationMinimizer(cout_sknf)
    cout_minimized_result = cout_minimizer.minimize()
    print("\nМинимизированная СКНФ для Cout:")
    print(cout_minimized_result['result'])

if __name__ == "__main__":
    main()