import itertools

class LogicExpressions:
    def __init__(self, expression):
        self.expression = expression
        self.variables = self._extract_variables(expression)
        self.table = self._generate_truth_table()

    def _extract_variables(self, expression):
        # Извлекаем уникальные переменные (буквы) из выражения
        variables = set()
        for char in expression:
            if char.isalpha():  # Проверяем, является ли символ буквой
                variables.add(char)
        return sorted(variables)

    def _evaluate(self, values):
        expr = self.expression
        for var, val in zip(self.variables, values):
            expr = expr.replace(var, str(val))
        expr = (expr.replace('!', ' not ')
                .replace('¬', ' not ')
                .replace('&', ' and ')
                .replace('∧', ' and ')
                .replace('|', ' or ')
                .replace('∨', ' or ')
                .replace('->', ' <= ')
                .replace('→', ' <= ')
                .replace('~', ' == ')
                .replace('↔', ' == '))

        return self._manual_eval(expr)

    def _manual_eval(self, expr):
        expr = expr.replace('(', ' ( ').replace(')', ' ) ')
        tokens = expr.split()
        output = []
        operators = []

        precedence = {'not': 3, 'and': 2, 'or': 1, '==': 1, '<=': 1}

        for token in tokens:
            if token in ('0', '1'):
                output.append(int(token))
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()
            elif token in precedence:
                while (operators and operators[-1] != '(' and
                       precedence.get(operators[-1], 0) >= precedence[token]):
                    output.append(operators.pop())
                operators.append(token)

        while operators:
            output.append(operators.pop())

        stack = []
        for token in output:
            if isinstance(token, int):
                stack.append(token)
            elif token == 'not':
                stack.append(1 - stack.pop())
            else:
                b = stack.pop()
                a = stack.pop()
                if token == 'and':
                    stack.append(a & b)
                elif token == 'or':
                    stack.append(a | b)
                elif token == '==':
                    stack.append(int(a == b))
                elif token == '<=':
                    stack.append(int(not a or b))
        return stack[0]

    def _generate_truth_table(self):
        table = []
        for values in itertools.product([0, 1], repeat=len(self.variables)):
            result = self._evaluate(values)
            table.append((values, result))
        return table

    def build_sdnf(self):
        terms = []
        indexes = []
        for index, (values, result) in enumerate(self.table):
            if result == 1:
                term = []
                for var, val in zip(self.variables, values):
                    term.append(f"{'¬' if val == 0 else ''}{var}")
                terms.append(f"({'∧'.join(term)})")
                indexes.append(str(index))
        return ' ∨ '.join(terms), f"({', '.join(indexes)})"

    def build_sknf(self):
        terms = []
        indexes = []
        for index, (values, result) in enumerate(self.table):
            if result == 0:
                term = []
                for var, val in zip(self.variables, values):
                    term.append(f"{'¬' if val == 1 else ''}{var}")
                terms.append(f"({'∨'.join(term)})")
                indexes.append(str(index))
        return ' ∧ '.join(terms), f"({', '.join(indexes)})"

    def calculate_index_form(self):
        bits = ''.join(str(result) for _, result in self.table)
        decimal_value = sum(int(bit) * (2 ** (len(bits) - 1 - i)) for i, bit in enumerate(bits))
        return f"{decimal_value} - {bits}"

    def print_truth_table(self):
        print("\nТаблица истинности:")
        header = ' | '.join(self.variables) + ' | Result'
        print(header)
        print('-' * len(header))
        for values, result in self.table:
            row = ' | '.join(map(str, values)) + ' | ' + str(result)
            print(row)
