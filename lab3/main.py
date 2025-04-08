from src.boolean_function import BooleanFunction
from src.karnaugh_minimizer import KarnaughMinimizer


def print_karnaugh_table(result, variables):
    table = result["table"]
    row_gray = result["row_gray"]
    col_gray = result["col_gray"]

    # Вывод заголовка с кодом Грея для столбцов
    print("Карта Карно:")
    print(f"{'':>4}", end="")  # Отступ для строкового заголовка
    for cg in col_gray:
        print(f"{cg:>4}", end="")
    print()  # Новая строка после заголовка

    # Вывод строк с кодом Грея для строк
    for i, row in enumerate(table):
        print(f"{row_gray[i]:>4}", end="")
        for val in row:
            print(f"{val:>4}", end="")
        print()  # Новая строка после каждой строки таблицы


# Примеры
examples = [
    {"type": "СДНФ", "terms": ["¬abc", "a¬b¬c", "a¬bc", "ab¬c", "abc"]},
    {"type": "СДНФ", "terms": ["¬a¬b¬c¬d", "¬a¬bc¬d", "abcd", "abc¬d"]},
    {"type": "СДНФ", "terms": ["¬a¬b¬c¬de", "¬a¬bcde", "abcd¬e", "abcde"]},
    {"type": "СКНФ", "terms": ["a∨b∨¬c", "a∨¬b∨¬c", "¬a∨¬b∨c"]},
]

for i, ex in enumerate(examples, 1):
    print(f"\n=== Пример {i}: {ex['type']} ===")
    print(
        f"Исходная {ex['type']}: {' ∨ '.join(ex['terms']) if ex['type'] == 'СДНФ' else ' ∧ '.join(f'({t})' for t in ex['terms'])}")
    bf = BooleanFunction(ex["terms"], ex["type"] == "СДНФ")  # Убираем variables
    minimizer = KarnaughMinimizer(bf)
    result = minimizer.minimize()
    # Используем переменные из объекта BooleanFunction
    variables = ''.join(bf.variables)
    print_karnaugh_table(result, variables)
    minimized = " ∨ ".join(result["result"]) if ex["type"] == "СДНФ" else " ∧ ".join(f"({t})" for t in result["result"])
    print(f"Минимизированная {'ДНФ' if ex['type'] == 'СДНФ' else 'КНФ'}: {minimized}")