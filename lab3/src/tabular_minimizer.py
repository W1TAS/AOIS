# from main import result
from src.boolean_function import BooleanFunction
from src.utils import glue_terms #, print_table  # Предполагаемый импорт ваших функций
from itertools import combinations

class TabularMinimizer:
    def __init__(self, function: BooleanFunction):
        self.function = function
        self.variables = ''.join(self.function.variables)  # Строковое представление для glue_terms
        self.initial_terms = self.function.terms.copy()  # Копия исходных термов
        self.is_dnf = self.function.is_dnf  # True для СДНФ, False для СКНФ

    def minimize(self):
        terms = self.function.terms
        prev_terms = []
        stage = 0
        stages = []
        while(set(terms)!= set(prev_terms)):
            stage += 1
            if stage > 100:  # Ограничение на случай бесконечного цикла
                print("Прервано: слишком много итераций")
                break
            prev_terms = terms
            terms = self._perform_gluing(terms)
            stages.append(terms.copy())
        stages.pop()
        coverage_table = self._build_coverage_table(terms)
        essential_implicants, updated_table = self._find_essential_implicants(coverage_table)
        necessary_terms = self._select_minimal_cover(updated_table, essential_implicants)
        result = self._format_result(necessary_terms)
        return {"stages": stages,"coverage_table":coverage_table, "result": result}

    def _perform_gluing(self, terms):
        new_terms = set()
        used_terms = set()
        for i, term1 in enumerate(terms):
            for term2 in terms[i + 1:]:
                result = glue_terms(term1, term2, self.variables)
                if result:
                    new_terms.add(result)
                    used_terms.add(term1)
                    used_terms.add(term2)
        remaining_terms = set(terms) - used_terms
        new_terms.update(remaining_terms)
        return list(new_terms)

    def _build_coverage_table(self, implicants):
        coverage_table = {}
        for implicant in implicants:
            coverage_table[implicant] = []
            for term in self.initial_terms:
                if self._covers(implicant, term):
                    coverage_table[implicant].append(term)
        return coverage_table

    def _find_essential_implicants(self, coverage_table):
        essential_implicants = set()  # Множество существенных импликант
        updated_table = coverage_table.copy()  # Копия таблицы

        # Считаем, сколько раз каждый терм покрывается
        term_coverage_count = {}
        for implicant, terms in coverage_table.items():
            for term in terms:
                term_coverage_count[term] = term_coverage_count.get(term, 0) + 1

        # Находим существенные импликанты
        covered_terms = set()  # Покрытые термы
        for implicant in coverage_table:
            # Проверяем, есть ли терм, покрытый только этой импликантой
            for term in coverage_table[implicant]:
                if term_coverage_count[term] == 1:
                    essential_implicants.add(implicant)
                    covered_terms.update(coverage_table[implicant])
                    break  # Импликанта уже существенна, переходим к следующей

        # Удаляем существенные импликанты и покрытые термы из updated_table
        for implicant in essential_implicants:
            updated_table.pop(implicant)
        for implicant in updated_table:
            updated_table[implicant] = [t for t in updated_table[implicant] if t not in covered_terms]

        return essential_implicants, updated_table

    def _select_minimal_cover(self, coverage_table, essential_implicants):
        # Шаг 1: Определяем термы, покрытые существенными импликантами
        covered_terms = set()
        for implicant in essential_implicants:
            for term in self.initial_terms:
                if self._covers(implicant, term):
                    covered_terms.add(term)

        # Шаг 2: Находим оставшиеся термы, которые нужно покрыть
        required_terms = set(self.initial_terms) - covered_terms

        # Шаг 3: Если все термы уже покрыты, возвращаем только существенные
        if not required_terms:
            return list(essential_implicants)

        # Шаг 4: Получаем все импликанты из coverage_table
        available_implicants = list(coverage_table.keys())

        # Шаг 5: Перебор всех возможных комбинаций импликант
        min_implicants = None
        min_count = float('inf')  # Минимальное количество импликант
        for r in range(1, len(available_implicants) + 1):  # От 1 до всех импликант
            for combo in combinations(available_implicants, r):
                # Проверяем, покрывает ли комбинация все required_terms
                combo_covered = set()
                for implicant in combo:
                    combo_covered.update(coverage_table[implicant])
                if required_terms.issubset(combo_covered):
                    # Если покрывает и меньше текущего минимума, обновляем
                    if r < min_count:
                        min_count = r
                        min_implicants = list(combo)
                    break  # Нашли покрытие для текущего размера, дальше не проверяем

        # Шаг 6: Объединяем с существенными импликантами
        if min_implicants is None:
            return list(essential_implicants)  # Если ничего не нужно, возвращаем только существенные
        return list(essential_implicants) + min_implicants

    def _covers(self, implicant, original_term):
        imp_bin = self.function.to_binary(implicant)
        term_bin = self.function.to_binary(original_term)
        for bit1, bit2 in zip(imp_bin, term_bin):
            if not (bit1 == bit2 or bit1 == "X"): return False
        return True

    def _format_result(self, terms):
        if self.is_dnf:
            # Для ДНФ: соединяем термы через ∨, убираем лишние ∧
            cleaned_terms = []
            for term in terms:
                term = term.replace("∧", "").replace("∨∨", "∨")  # Убираем ∧ и лишние ∨
                if term:
                    literals = [lit for lit in term.split("∨") if lit]  # Разделяем на литералы
                    cleaned_term = "∧".join(literals)  # В ДНФ литералы в терме соединяются ∧
                    cleaned_terms.append(f"{cleaned_term}")
            return " ∨ ".join(cleaned_terms) if cleaned_terms else "0"
        else:
            # Для СКНФ: соединяем термы через ∧, каждый терм — дизъюнкция литералов
            formatted_terms = []
            for term in terms:
                # Убираем лишние ∨ и ∧
                term = term.replace("∨∨", "∨").replace("∧", "")
                literals = []
                i = 0
                while i < len(term):
                    if term[i] == "¬":
                        literals.append(term[i:i + 2])  # Берем ¬ и букву
                        i += 2
                    elif term[i].isalpha():
                        literals.append(term[i])  # Берем одиночную букву
                        i += 1
                    else:
                        i += 1  # Пропускаем лишние символы
                literals = [lit for lit in literals if lit]  # Убираем пустые литералы
                if literals:
                    disjunction = "∨".join(literals)
                    formatted_terms.append(f"({disjunction})")
            return " ∧ ".join(formatted_terms) if formatted_terms else "1"