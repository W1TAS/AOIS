from src.boolean_function import BooleanFunction
from src.utils import glue_terms  # Предполагаемый импорт вашей функции


class CalculationMinimizer:
    def __init__(self, function: BooleanFunction):
        self.function = function
        self.variables = ''.join(self.function.variables)  # Строковое представление для glue_terms
        self.initial_terms = self.function.terms.copy()  # Копия исходных термов
        self.is_dnf = self.function.is_dnf  # True для СДНФ, False для СКНФ

    def minimize(self):
        terms = self.function.terms.copy()
        prev_terms = []
        stages = []
        stage = 0
        while set(terms) != set(prev_terms):
            stage += 1
            if stage > 100:
                print("Прервано: слишком много итераций")
                break
            prev_terms = terms.copy()
            terms = self._perform_gluing(terms)
            stages.append(terms.copy())
        if stages:
            stages.pop()

        # Итеративное удаление с приоритетом минимальности
        final_implicants = terms.copy()
        changed = True
        while changed:
            changed = False
            # Сортируем по длине, чтобы сначала проверять более длинные
            final_implicants.sort(key=len, reverse=True)
            for i in range(len(final_implicants)):
                implicant = final_implicants[i]
                if self._is_redundant(implicant, final_implicants):
                    final_implicants.pop(i)
                    changed = True
                    break

        result = self._format_result(final_implicants)
        return {"stages": stages, "result": result}


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

    def _is_redundant(self, implicant, current_implicants):
        # Создаём список импликант без текущей
        remaining_implicants = [imp for imp in current_implicants if imp != implicant]
        if not remaining_implicants:  # Если ничего не осталось, импликанта не лишняя
            return False

        # Проверяем, покрываются ли все исходные термы оставшимися импликантами
        for term in self.initial_terms:
            if not any(self._covers(other_imp, term) for other_imp in remaining_implicants):
                return False  # Если хоть один терм не покрыт, импликанта нужна
        return True  # Все исходные термы покрыты без этой импликанты

    def _covers(self, implicant, original_term):
        imp_bin = self.function.to_binary(implicant)
        term_bin = self.function.to_binary(original_term)
        for bit1, bit2 in zip(imp_bin, term_bin):
            if not (bit1 == bit2 or bit1 == "X"): return False
        return True


    def _format_result(self, terms):
        if self.is_dnf: return " ∨ ".join(terms)
        else:
            # Для СКНФ: обрабатываем термы с учётом их формата
            formatted_terms = []
            for term in terms:
                if "∨" in term:
                    # Если терм уже содержит дизъюнкцию, просто оборачиваем в скобки
                    formatted_terms.append(f"({term})")
                else:
                    # Если терм без дизъюнкции (например, "a¬c"), преобразуем в "a∨¬c"
                    literals = []
                    i = 0
                    while i < len(term):
                        if term[i] == "¬":
                            literals.append(term[i:i + 2])  # Берем ¬ и букву
                            i += 2
                        else:
                            literals.append(term[i])  # Берем одиночную букву
                            i += 1
                    disjunction = "∨".join(literals)
                    formatted_terms.append(f"({disjunction})")
            return " ∧ ".join(formatted_terms)