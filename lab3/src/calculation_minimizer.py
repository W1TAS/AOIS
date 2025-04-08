from src.boolean_function import BooleanFunction
from src.utils import glue_terms  # Предполагаемый импорт вашей функции


class CalculationMinimizer:
    def __init__(self, function: BooleanFunction):
        self.function = function
        self.variables = ''.join(self.function.variables)  # Строковое представление для glue_terms
        self.initial_terms = self.function.terms.copy()  # Копия исходных термов
        self.is_dnf = self.function.is_dnf  # True для СДНФ, False для СКНФ

    def minimize(self):
        terms = self.function.terms
        prev_terms = []
        stage = 0
        while(terms!= prev_terms):
            stage += 1
            prev_terms = terms
            terms = self._perform_gluing(terms)
            print(f"Этап - {stage}: {terms}")
        necessary_terms = set()
        for term in terms:
            if self._is_redundant(term, set(terms)-{term}):
                continue
            else:
                necessary_terms.add(term)
        return self._format_result(necessary_terms)

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

    def _is_redundant(self, implicant, other_implicants):
        return any(self._covers(other_implicant, implicant) for other_implicant in other_implicants)


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