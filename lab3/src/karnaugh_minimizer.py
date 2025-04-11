from src.boolean_function import BooleanFunction
from itertools import combinations
from src.utils import glue_terms, print_table
import math
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def generate_gray_code(n):
    if n <= 0:
        return [[]]
    prev = generate_gray_code(n - 1)
    result = [[0] + code for code in prev] + [[1] + code for code in prev[::-1]]
    logger.info(f"Generated Gray code for {n} bits: {result}")
    return result

class KarnaughMinimizer:
    def __init__(self, function: BooleanFunction):
        self.function = function
        self.variables = self.function.variables
        self.num_vars = len(self.variables)
        self.cols = 2 ** math.ceil(self.num_vars / 2)
        self.rows = 2 ** (self.num_vars - math.ceil(self.num_vars / 2))
        self.map = None
        self.is_dnf = self.function.is_dnf
        logger.info(f"Initialized with {self.num_vars} vars: rows={self.rows}, cols={self.cols}")

    def minimize(self):
        logger.info("Starting minimization")
        self.map = self._build_karnaugh_map()
        # Сохраняем коды Грея для возврата
        col_vars = math.ceil(self.num_vars / 2)
        row_vars = self.num_vars - col_vars
        row_gray = [''.join(map(str, code)) for code in generate_gray_code(row_vars)]
        col_gray = [''.join(map(str, code)) for code in generate_gray_code(col_vars)]
        groups = self._find_groups()
        result = self._terms_from_groups(groups)
        real_result = self._format_result(result)
        logger.info(f"Minimization completed. Result: {result}")
        return {
            "table": self.map,
            "row_gray": row_gray,  # Код Грея для строк
            "col_gray": col_gray,  # Код Грея для столбцов
            "result": real_result
        }

    def _build_karnaugh_map(self):
        default_value = 1 if not self.function.is_dnf else 0
        kmap = [[default_value] * self.cols for _ in range(self.rows)]
        col_vars = math.ceil(self.num_vars / 2)
        row_vars = self.num_vars - col_vars
        row_gray = [list(map(int, code)) for code in generate_gray_code(row_vars)]
        col_gray = [list(map(int, code)) for code in generate_gray_code(col_vars)]
        logger.info(f"Building map: row_vars={row_vars}, col_vars={col_vars}")
        logger.info(f"Row Gray code: {row_gray}")
        logger.info(f"Col Gray code: {col_gray}")

        for term in self.function.terms:
            bin_rep = self.function.to_binary(term)
            logger.info(f"Processing term {term} -> binary: {bin_rep}")
            row_vals = [0 if bin_rep[i] == "0" else 1 if bin_rep[i] == "1" else None
                        for i in range(row_vars)]
            col_vals = [0 if bin_rep[i] == "0" else 1 if bin_rep[i] == "1" else None
                        for i in range(row_vars, self.num_vars)]

            for r_idx, row in enumerate(row_gray):
                for c_idx, col in enumerate(col_gray):
                    if all(row_vals[i] is None or row_vals[i] == row[i] for i in range(row_vars)) and \
                       all(col_vals[i] is None or col_vals[i] == col[i] for i in range(col_vars)):
                        kmap[r_idx][c_idx] = 1 if self.function.is_dnf else 0
                        logger.debug(f"Set kmap[{r_idx}][c_idx] = {kmap[r_idx][c_idx]}")
        logger.info("Karnaugh map built:")
        for row in kmap:
            logger.info(f"Row: {row}")
        return kmap

    def _find_groups(self):
        kmap = self.map
        target = 1 if self.function.is_dnf else 0
        all_targets = {(r, c) for r in range(self.rows) for c in range(self.cols) if kmap[r][c] == target}
        logger.info(f"Finding groups for target={target}. Targets: {all_targets}")

        # Шаг 1: Собираем все возможные группы
        possible_groups = []
        for height in [2 ** i for i in range(int(math.log2(self.rows)) + 1)]:
            for width in [2 ** i for i in range(int(math.log2(self.cols)) + 1)]:
                logger.debug(f"Checking size {height}x{width}")
                for r_start in range(self.rows):
                    for c_start in range(self.cols):
                        valid = True
                        cells = set()
                        for i in range(height):
                            for j in range(width):
                                r = (r_start + i) % self.rows
                                c = (c_start + j) % self.cols
                                if kmap[r][c] != target:
                                    valid = False
                                    break
                                cells.add((r, c))
                            if not valid:
                                break
                        if valid and cells.issubset(all_targets):
                            possible_groups.append((r_start, (r_start + height - 1) % self.rows,
                                                    c_start, (c_start + width - 1) % self.cols))
                            logger.debug(f"Found group: {possible_groups[-1]}")

        logger.info(f"All possible groups: {possible_groups}")

        # Шаг 2: Находим все покрытия с минимальным числом групп
        min_count = float('inf')
        candidate_covers = []
        for r in range(1, len(possible_groups) + 1):
            for combo in combinations(possible_groups, r):
                covered = set()
                for group in combo:
                    covered.update(self._get_group_cells(group))
                if all_targets.issubset(covered):
                    candidate_covers.append(list(combo))
                    min_count = r
                    logger.info(f"Found cover with {r} groups: {combo}")
            if candidate_covers:  # Прерываем, как только нашли покрытия с минимальным r
                break

        # Шаг 3: Выбираем покрытие с минимальной суммарной длиной импликант
        def get_terms_length(groups):
            terms = self._terms_from_groups(groups)
            return sum(len(term) for term in terms)

        min_length = float('inf')
        best_groups = None
        for cover in candidate_covers:
            length = get_terms_length(cover)
            if length < min_length:
                min_length = length
                best_groups = cover
                logger.info(f"Updated best cover: {best_groups}, length={min_length}")

        logger.info(f"Minimal groups with shortest terms: {best_groups}")
        return best_groups or []

    def _get_group_cells(self, group):
        r_start, r_end, c_start, c_end = group
        if r_start <= r_end:
            rows = range(r_start, r_end + 1)
        else:
            rows = list(range(r_start, self.rows)) + list(range(0, r_end + 1))
        if c_start <= c_end:
            cols = range(c_start, c_end + 1)
        else:
            cols = list(range(c_start, self.cols)) + list(range(0, c_end + 1))
        return {(r, c) for r in rows for c in cols}

    def _terms_from_groups(self, groups):
        row_vars = self.num_vars - math.ceil(self.num_vars / 2)
        col_vars = math.ceil(self.num_vars / 2)
        row_gray = [list(map(int, code)) for code in generate_gray_code(row_vars)]
        col_gray = [list(map(int, code)) for code in generate_gray_code(col_vars)]
        terms = []

        for r_start, r_end, c_start, c_end in groups:
            term = ""
            if r_start <= r_end:
                rows = range(r_start, r_end + 1)
            else:
                rows = list(range(r_start, self.rows)) + list(range(0, r_end + 1))
            if c_start <= c_end:
                cols = range(c_start, c_end + 1)
            else:
                cols = list(range(c_start, self.cols)) + list(range(0, c_end + 1))
            row_bits = [set(row_gray[r][i] for r in rows) for i in range(row_vars)]
            col_bits = [set(col_gray[c][i] for c in cols) for i in range(col_vars)]
            logger.debug(f"Group ({r_start}, {r_end}, {c_start}, {c_end}): row_bits={row_bits}, col_bits={col_bits}")

            # Для СКНФ инвертируем логику: группа нулей -> дизъюнкция противоположных значений
            if self.function.is_dnf:
                # СДНФ: прямые значения
                for i, bits in enumerate(row_bits):
                    if len(bits) == 1:
                        val = bits.pop()
                        term += self.variables[i] if val == 1 else f"¬{self.variables[i]}"
                    else:
                        logger.debug(f"Var {self.variables[i]} varies, skipping")
                for i, bits in enumerate(col_bits):
                    if len(bits) == 1:
                        val = bits.pop()
                        term += self.variables[row_vars + i] if val == 1 else f"¬{self.variables[row_vars + i]}"
                    else:
                        logger.debug(f"Var {self.variables[row_vars + i]} varies, skipping")
            else:
                # СКНФ: инвертированные значения
                for i, bits in enumerate(row_bits):
                    if len(bits) == 1:
                        val = bits.pop()
                        term += f"¬{self.variables[i]}" if val == 1 else self.variables[i]
                    else:
                        logger.debug(f"Var {self.variables[i]} varies, skipping")
                for i, bits in enumerate(col_bits):
                    if len(bits) == 1:
                        val = bits.pop()
                        term += f"¬{self.variables[row_vars + i]}" if val == 1 else self.variables[row_vars + i]
                    else:
                        logger.debug(f"Var {self.variables[row_vars + i]} varies, skipping")
            terms.append(term)
            logger.info(f"Generated term: {term}")
        return terms

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