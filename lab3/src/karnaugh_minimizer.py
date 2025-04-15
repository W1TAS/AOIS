import logging
from itertools import combinations

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_gray_code(n):
    if n <= 0:
        return [[]]
    prev = generate_gray_code(n - 1)
    return [[0] + code for code in prev] + [[1] + code for code in prev[::-1]]

def hamming_distance(a, b):
    return sum(c1 != c2 for c1, c2 in zip(a, b))

class KarnaughMinimizer:
    def __init__(self, function):
        self.function = function
        self.variables = function.variables
        self.num_vars = len(self.variables)
        self.is_dnf = function.is_dnf
        self.row_vars = 2 if self.num_vars >= 4 else min(self.num_vars, 1)
        self.col_vars = self.num_vars - self.row_vars
        self.rows = 2 ** self.row_vars
        self.cols = 2 ** self.col_vars
        self.map = None
        self.graph = None
        self.targets = None

    def build_karnaugh_map(self):
        self.map = self._build_karnaugh_map()
        return self.map

    def _build_karnaugh_map(self):
        default_value = 0 if self.is_dnf else 1
        kmap = [[default_value] * self.cols for _ in range(self.rows)]
        row_gray = generate_gray_code(self.row_vars)
        col_gray = generate_gray_code(self.col_vars)

        for r_idx, row in enumerate(row_gray):
            for c_idx, col in enumerate(col_gray):
                binary = row + col
                assignment = {self.variables[i]: int(binary[i]) for i in range(self.num_vars)}
                result = self.function.evaluate_term(assignment)
                kmap[r_idx][c_idx] = 1 if result else 0
        return kmap

    def build_graph(self):
        self.graph = self._build_graph()
        return self.graph

    def _build_graph(self):
        graph = {}
        row_gray = generate_gray_code(self.row_vars)
        col_gray = generate_gray_code(self.col_vars)

        for r in range(self.rows):
            for c in range(self.cols):
                graph[(r, c)] = set()

        for r1 in range(self.rows):
            for c1 in range(self.cols):
                binary1 = ''.join(map(str, row_gray[r1] + col_gray[c1]))
                for r2 in range(self.rows):
                    for c2 in range(self.cols):
                        if (r1, c1) != (r2, c2):
                            binary2 = ''.join(map(str, row_gray[r2] + col_gray[c2]))
                            if hamming_distance(binary1, binary2) == 1:
                                graph[(r1, c1)].add((r2, c2))
                                graph[(r2, c2)].add((r1, c1))
        return graph

    def find_groups(self):
        if self.map is None:
            self.map = self._build_karnaugh_map()
        if self.graph is None:
            self.graph = self._build_graph()
        return self._find_groups()

    def _find_groups(self):
        target = 1 if self.is_dnf else 0
        self.targets = {(r, c) for r in range(self.rows) for c in range(self.cols) if self.map[r][c] == target}
        if not self.targets:
            return []

        row_gray = generate_gray_code(self.row_vars)
        col_gray = generate_gray_code(self.col_vars)
        groups = []
        covered = set()

        for size in sorted([2**i for i in range(self.num_vars + 1)], reverse=True):
            for subset in combinations(self.targets, size):
                subset = set(subset)
                if not self._is_valid_group(subset):
                    continue

                binaries = {''.join(map(str, row_gray[r] + col_gray[c])) for r, c in subset}
                combined = ['-'] * self.num_vars
                for i in range(self.num_vars):
                    bits = {binary[i] for binary in binaries}
                    if len(bits) == 1:
                        combined[i] = bits.pop()

                fixed_positions = [(i, bit) for i, bit in enumerate(combined) if bit != '-']
                if not fixed_positions:
                    continue

                valid_subset = set()
                for r, c in self.targets:
                    binary = ''.join(map(str, row_gray[r] + col_gray[c]))
                    if all(binary[i] == bit for i, bit in fixed_positions):
                        valid_subset.add((r, c))

                if len(valid_subset) != size:
                    continue

                if valid_subset.issubset(covered):
                    continue

                groups.append(valid_subset)
                covered.update(valid_subset)

        for r, c in self.targets:
            if (r, c) not in covered:
                groups.append({(r, c)})
                covered.add((r, c))

        groups.sort(key=len, reverse=True)

        all_targets = set(self.targets)
        selected_groups = []
        covered = set()
        while all_targets - covered:
            best_group = None
            best_coverage = None
            best_term = None
            for component in groups:
                if component.issubset(covered):
                    continue
                new_coverage = component - covered
                if not new_coverage:
                    continue

                is_essential = any((r, c) in component for r, c in all_targets if (r, c) not in covered)

                binaries = {''.join(map(str, row_gray[r] + col_gray[c])) for r, c in component}
                combined = ['-'] * self.num_vars
                for i in range(self.num_vars):
                    bits = {binary[i] for binary in binaries}
                    if len(bits) == 1:
                        combined[i] = bits.pop()
                num_fixed = sum(1 for bit in combined if bit != '-')
                term_score = (len(new_coverage), -num_fixed)

                if is_essential:
                    if best_coverage is None:
                        best_group = component
                        best_coverage = new_coverage
                        best_term = combined
                    elif term_score > (len(best_coverage), -sum(1 for bit in best_term if bit != '-')):
                        best_group = component
                        best_coverage = new_coverage
                        best_term = combined

            if best_group:
                selected_groups.append(best_group)
                covered.update(best_group)
            else:
                for r, c in all_targets - covered:
                    selected_groups.append({(r, c)})
                    covered.add((r, c))
                break

        return selected_groups

    def _is_valid_group(self, component):
        if not component:
            return False

        def dfs(start, visited):
            stack = [start]
            reachable = set()
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    reachable.add(node)
                    stack.extend(n for n in self.graph[node] if n in component and n not in visited)
            return reachable

        start = next(iter(component))
        visited = set()
        reachable = dfs(start, visited)
        if len(reachable) != len(component):
            return False

        row_gray = generate_gray_code(self.row_vars)
        col_gray = generate_gray_code(self.col_vars)
        binaries = {''.join(map(str, row_gray[r] + col_gray[c])) for r, c in component}
        combined = ['-'] * self.num_vars
        for i in range(self.num_vars):
            bits = {binary[i] for binary in binaries}
            if len(bits) == 1:
                combined[i] = bits.pop()

        return True

    def terms_from_groups(self, groups):
        return self._terms_from_groups(groups)

    def _terms_from_groups(self, groups):
        row_gray = generate_gray_code(self.row_vars)
        col_gray = generate_gray_code(self.col_vars)
        terms = []

        for component in groups:
            if not component:
                continue

            binaries = set()
            for r, c in component:
                binary = ''.join(map(str, row_gray[r] + col_gray[c]))
                binaries.add(binary)

            term = []
            combined = ['-'] * self.num_vars
            for i in range(self.num_vars):
                bits = {binary[i] for binary in binaries}
                if len(bits) == 1:
                    combined[i] = bits.pop()
            for i, bit in enumerate(combined):
                if bit == '1':
                    term.append(self.variables[i] if self.is_dnf else f"¬{self.variables[i]}")
                elif bit == '0':
                    term.append(f"¬{self.variables[i]}" if self.is_dnf else self.variables[i])
            term_str = ''.join(term)
            if term_str:
                terms.append(term_str)
        return terms

    def format_result(self, terms):
        return self._format_result(terms)

    def _format_result(self, terms):
        if not terms:
            return "0" if self.is_dnf else "1"
        if self.is_dnf:
            return " ∨ ".join(terms)
        else:
            formatted_terms = []
            for term in terms:
                literals = []
                i = 0
                while i < len(term):
                    if term[i] == "¬":
                        literals.append(term[i:i + 2])
                        i += 2
                    else:
                        literals.append(term[i])
                        i += 1
                formatted_terms.append(f"({'∨'.join(literals)})")
            return " ∧ ".join(formatted_terms)

    def minimize(self):
        # Шаг 1: Построение карты Карно
        kmap = self.build_karnaugh_map()
        row_gray = [''.join(map(str, code)) for code in generate_gray_code(self.row_vars)]
        col_gray = [''.join(map(str, code)) for code in generate_gray_code(self.col_vars)]

        # Шаг 2: Поиск групп
        groups = self.find_groups()

        # Шаг 3: Формирование термов
        terms = self.terms_from_groups(groups)

        # Шаг 4: Форматирование результата
        result = self.format_result(terms)

        # Шаг 5: Формирование возвращаемого словаря
        return {
            'result': result,
            'table': kmap,
            'row_gray': [f"{'ab' if self.row_vars == 2 else self.variables[0]}={code}" for code in row_gray],
            'col_gray': [f"{'cde' if self.col_vars == 3 else ''.join(self.variables[self.row_vars:])}={code}" for code in col_gray]
        }