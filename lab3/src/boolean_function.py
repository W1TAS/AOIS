class BooleanFunction:
    def __init__(self, terms, is_dnf=True):
        self.terms = terms
        self.is_dnf = is_dnf
        self.variables = self._extract_variables()

    def _extract_variables(self):
        vars_set = set()
        for term in self.terms:
            for char in term:
                if char.isalpha():
                    vars_set.add(char)
        return sorted(vars_set)

    def to_binary(self, term):
        if self.is_dnf:
            # Для СДНФ: прямое преобразование терма
            binary = ""
            for var in self.variables:
                if f"¬{var}" in term:
                    binary += "0"
                elif var in term:
                    binary += "1"
                else:
                    binary += "X"
            return binary
        else:
            # Для СКНФ: точка, где терм ложен (все литералы ложны)
            binary = ""
            for var in self.variables:
                if f"¬{var}" in term:
                    binary += "1"  # ¬a=0 значит a=1
                elif var in term:
                    binary += "0"  # a=0
                else:
                    binary += "X"
            return binary

    def __str__(self):
        return " ∨ ".join(self.terms) if self.is_dnf else " ∧ ".join(self.terms)