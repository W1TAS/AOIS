from src.boolean_function import BooleanFunction
from src.calculation_minimizer import CalculationMinimizer

# Таблица истинности для преобразователя Д8421 → Д8421+5
# A, B, C, D — входы
# W, X, Y, Z — выходы
truth_table_data = [
    (0, 0, 0, 0, 0, 1, 0, 1),  # 0 → 5
    (0, 0, 0, 1, 0, 1, 1, 0),  # 1 → 6
    (0, 0, 1, 0, 0, 1, 1, 1),  # 2 → 7
    (0, 0, 1, 1, 1, 0, 0, 0),  # 3 → 8
    (0, 1, 0, 0, 1, 0, 0, 1),  # 4 → 9
    (0, 1, 0, 1, 0, 0, 0, 0),  # 5 → 0
    (0, 1, 1, 0, 0, 0, 0, 1),  # 6 → 1
    (0, 1, 1, 1, 0, 0, 1, 0),  # 7 → 2
    (1, 0, 0, 0, 0, 0, 1, 1),  # 8 → 3
    (1, 0, 0, 1, 0, 1, 0, 0),  # 9 → 4
    (1, 0, 1, 0, None, None, None, None),  # Недопустимый
    (1, 0, 1, 1, None, None, None, None),
    (1, 1, 0, 0, None, None, None, None),
    (1, 1, 0, 1, None, None, None, None),
    (1, 1, 1, 0, None, None, None, None),
    (1, 1, 1, 1, None, None, None, None)
]

def print_truth_table():
    """Выводит таблицу истинности для преобразователя Д8421 → Д8421+5."""
    print("\nТаблица истинности для преобразователя Д8421 → Д8421+5:")
    header = "A | B | C | D | W | X | Y | Z"
    print(header)
    print("-" * len(header))
    for row in truth_table_data:
        w = 'X' if row[4] is None else row[4]
        x = 'X' if row[5] is None else row[5]
        y = 'X' if row[6] is None else row[6]
        z = 'X' if row[7] is None else row[7]
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {w} | {x} | {y} | {z}")

def build_sknf_for_output(table, output_index, variables):
    """Строит СКНФ для указанного выхода, игнорируя неопределённые состояния."""
    terms = []
    for row in table:
        if row[output_index] == 0:  # Для СКНФ берём строки, где выход = 0
            term = []
            for var, val in zip(variables, row[:4]):  # Берём только входы A, B, C, D
                term.append(f"{'¬' if val == 1 else ''}{var}")
            terms.append(f"({'∨'.join(term)})")
    return terms

def main():
    # Вывод таблицы истинности
    print_truth_table()

    # Переменные
    variables = ['A', 'B', 'C', 'D']

    # Построение и минимизация СКНФ для каждого выхода (W, X, Y, Z)
    for i, output_name in enumerate(['W', 'X', 'Y', 'Z']):
        output_index = 4 + i  # W=4, X=5, Y=6, Z=7
        terms = build_sknf_for_output(truth_table_data, output_index, variables)
        sknf = BooleanFunction(terms, is_dnf=False)
        print(f"\nСКНФ для {output_name}:")
        print(sknf)

        # Минимизация СКНФ
        minimizer = CalculationMinimizer(sknf)
        minimized_result = minimizer.minimize()
        print(f"\nМинимизированная СКНФ для {output_name}:")
        print(minimized_result['result'])

if __name__ == "__main__":
    main()