import argparse
from LogicExpression import LogicExpressions

def main():
    parser = argparse.ArgumentParser(description="Обработка логических выражений")
    parser.add_argument("expression", type=str, nargs="?", help="Логическое выражение")
    args = parser.parse_args()

    expression = args.expression or input("Введите логическое выражение: ")

    logic = LogicExpressions(expression)

    sdnf, sdnf_indices = logic.build_sdnf()
    sknf, sknf_indices = logic.build_sknf()
    index_form = logic.calculate_index_form()

    logic.print_truth_table()
    print(f"СДНФ: {sdnf}")
    print(f"Числовая форма СДНФ: {sdnf_indices}")
    print(f"СКНФ: {sknf}")
    print(f"Числовая форма СКНФ: {sknf_indices}")
    print(f"Индексная форма: {index_form}")

if __name__ == "__main__":
    main()