from src.boolean_function import BooleanFunction
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
        logger.info(f"Minimization completed. Result: {result}")
        return {
            "table": self.map,
            "row_gray": row_gray,  # Код Грея для строк
            "col_gray": col_gray,  # Код Грея для столбцов
            "result": result
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

        groups = []
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
                            groups.append((r_start, (r_start + height - 1) % self.rows,
                                           c_start, (c_start + width - 1) % self.cols))
                            logger.debug(f"Found group: {groups[-1]}")

        groups.sort(key=lambda g: ((g[1] - g[0] + 1) % self.rows or self.rows) *
                                  ((g[3] - g[2] + 1) % self.cols or self.cols), reverse=True)
        logger.info(f"All groups sorted: {groups}")

        essential = []
        uncovered = all_targets.copy()
        while uncovered and groups:
            best_group = max(groups, key=lambda g: len(self._get_group_cells(g) & uncovered))
            covered = self._get_group_cells(best_group)
            if covered & uncovered:
                essential.append(best_group)
                uncovered -= covered
                logger.info(f"Added group {best_group}. Uncovered: {uncovered}")
            groups.remove(best_group)

        logger.info(f"Essential groups: {essential}")
        return essential

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