from src.logic_expression import LogicExpressions
from src.calculation_minimizer import CalculationMinimizer
from src.tabular_minimizer import TabularMinimizer
from src.karnaugh_minimizer import KarnaughMinimizer
from src.boolean_function import BooleanFunction
from src.utils import print_table


def minimize_expression(expression):
    # Шаг 1: Создаём объект LogicExpressions
    logic = LogicExpressions(expression)
    print(f"\nИсходное выражение: {expression}")
    logic.print_truth_table()

    # Шаг 2: Получаем СДНФ и СКНФ
    sdnf, sdnf_indexes = logic.build_sdnf()
    sknf, sknf_indexes = logic.build_sknf()
    print(f"\nСДНФ: {sdnf}")
    print(f"Индексы СДНФ: {sdnf_indexes}")
    print(f"СКНФ: {sknf}")
    print(f"Индексы СКНФ: {sknf_indexes}")

    # Шаг 3: Преобразуем СДНФ и СКНФ в списки термов
    sdnf_terms = [term.strip('()') for term in sdnf.split(' ∨ ')]
    sknf_terms = [term.strip('()') for term in sknf.split(' ∧ ')]

    # Шаг 4: Создаём объекты BooleanFunction
    sdnf_func = BooleanFunction(sdnf_terms, is_dnf=True)
    sknf_func = BooleanFunction(sknf_terms, is_dnf=False)

    # Шаг 5: Минимизация всеми тремя методами
    minimizers = [
        ("Расчётный метод", CalculationMinimizer),
        ("Расчётно-табличный метод", TabularMinimizer),
        ("Метод Карно", KarnaughMinimizer),
    ]

    print("\n=== Минимизация СДНФ ===")
    for name, MinimizerClass in minimizers:
        minimizer = MinimizerClass(sdnf_func)
        result = minimizer.minimize()
        print(f"{name}:")

        if name == "Расчётный метод":
            print("Этапы:")
            for i, stage in enumerate(result.get("stages", []), 1):
                print(f"Этап {i}: {', '.join(stage)}")
        elif name == "Расчётно-табличный метод":
            print("Этапы:")
            for i, stage in enumerate(result.get("stages", []), 1):
                print(f"Этап {i}: {', '.join(stage)}")
            if 'coverage_table' in result:
                print_table(table=result['coverage_table'], orig_terms=sdnf_terms,
                            imp_terms=list(result['coverage_table'].keys()))
        elif name == "Метод Карно":
            if 'table' in result:
                print_table(headers=[""] + result["col_gray"],
                            rows=[[row_gray] + row for row_gray, row in zip(result["row_gray"], result["table"])])

        print(f"Результат: {result['result']}")
        print()

    print("=== Минимизация СКНФ ===")
    for name, MinimizerClass in minimizers:
        minimizer = MinimizerClass(sknf_func)
        result = minimizer.minimize()
        print(f"{name}:")

        if name == "Расчётный метод":
            print("Этапы:")
            for i, stage in enumerate(result.get("stages", []), 1):
                print(f"Этап {i}: {', '.join(stage)}")
        elif name == "Расчётно-табличный метод":
            print("Этапы:")
            for i, stage in enumerate(result.get("stages", []), 1):
                print(f"Этап {i}: {', '.join(stage)}")
            if 'coverage_table' in result:
                print_table(table=result['coverage_table'], orig_terms=sknf_terms,
                            imp_terms=list(result['coverage_table'].keys()))
        elif name == "Метод Карно":
            if 'table' in result:
                print_table(headers=[""] + result["col_gray"],
                            rows=[[row_gray] + row for row_gray, row in zip(result["row_gray"], result["table"])])

        print(f"Результат: {result['result']}")
        print()


def main():
    while True:
        expression = input("Введите логическое выражение (или 'exit' для выхода): ")
        if expression.lower() == 'exit':
            break
        try:
            minimize_expression(expression)
        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()