import random

class Matrix:
    def __init__(self, size=16):
        """Инициализация случайной матрицы size x size (слова — столбцы)."""
        self.size = size
        self.matrix = [[random.randint(0, 1) for _ in range(size)] for _ in range(size)]
        self.g = [[0 for _ in range(size + 1)] for _ in range(size)]  # Увеличен размер для n+1
        self.l = [[0 for _ in range(size + 1)] for _ in range(size)]  # Увеличен размер для n+1

    def get_word(self, j):
        """Получить слово (столбец) j с учетом диагональной адресации."""
        word = []
        for i in range(self.size):
            row = (i + j) % self.size  # Смещение на j для диагональной адресации
            word.append(self.matrix[row][j])
        return word

    def set_word(self, j, word):
        """Установить слово (столбец) j с учетом диагональной адресации."""
        for i in range(self.size):
            row = (i + j) % self.size  # Смещение на j
            self.matrix[row][j] = word[i]

    def display_matrix(self):
        """Вывести матрицу и слова (столбцы)."""
        print("Матрица:")
        for i in range(self.size):
            print("".join(str(self.matrix[i][j]) for j in range(self.size)))
        print("\nСлова (столбцы, с учетом диагональной адресации):")
        for j in range(self.size):
            word = self.get_word(j)
            print(f"Слово {j}: {''.join(str(bit) for bit in word)}")

    def display_word(self, j):
        """Вывести слово по индексу столбца j."""
        if 0 <= j < self.size:
            word = self.get_word(j)
            return f"Слово {j}: {''.join(str(bit) for bit in word)}"
        else:
            return f"Ошибка: столбец {j} вне диапазона (0..{self.size-1})"

    def compute_gl(self, argument):
        """Вычислить g_ji и l_ji для сравнения слова с аргументом."""
        n = self.size - 1
        for j in range(self.size):
            self.g[j][n + 1] = 0  # Начальные условия
            self.l[j][n + 1] = 0

        for i in range(n, -1, -1):
            a_i = (argument >> i) & 1
            for j in range(self.size):
                row = (i + j) % self.size  # Учитываем смещение
                s_ji = self.matrix[row][j]
                g_next = self.g[j][i + 1]
                l_next = self.l[j][i + 1]
                self.g[j][i] = g_next & (~a_i & s_ji & ~l_next)
                self.l[j][i] = l_next | (a_i & s_ji & g_next)

    def search_by_match(self, argument):
        """Поиск по соответствию: найти слова с максимальным числом совпадений."""
        self.compute_gl(argument)
        max_matches = 0
        matching_words = []
        for j in range(self.size):
            word = self.get_word(j)
            matches = sum(1 for i in range(self.size) if word[i] == ((argument >> i) & 1))
            if matches > max_matches:
                max_matches = matches
                matching_words = [j]
            elif matches == max_matches:
                matching_words.append(j)
        return matching_words, max_matches

    def logical_operation(self, func_id, col1, col2, target_col):
        """Выполнить логическую функцию func_id для столбцов col1 и col2, записать в target_col."""
        if not (0 <= col1 < self.size and 0 <= col2 < self.size and 0 <= target_col < self.size):
            return f"Ошибка: столбцы {col1}, {col2}, {target_col} должны быть в диапазоне 0..{self.size-1}"

        word1 = self.get_word(col1)
        word2 = self.get_word(col2)
        result = [0] * self.size

        for i in range(self.size):
            x1 = word1[i]
            x2 = word2[i]
            if func_id == 0:
                result[i] = 0
            elif func_id == 5:
                result[i] = x2
            elif func_id == 10:
                result[i] = int(not x2)
            elif func_id == 15:
                result[i] = 1
            else:
                return f"Ошибка: функция f{func_id} не поддерживается (доступны f0, f5, f10, f15)"

        self.set_word(target_col, result)
        return f"Операция f{func_id} выполнена: столбцы {col1} и {col2} -> столбец {target_col}"

    def extract_bits(self, column, start, end):
        """Извлечь биты с позиций start по end из столбца."""
        value = 0
        for i in range(start, end + 1):
            value = (value << 1) | column[i]
        return value

    def set_bits(self, column, start, end, value):
        """Установить биты с позиций start по end в столбце."""
        for i in range(end, start - 1, -1):
            column[i] = value & 1
            value >>= 1
        return column

    def add_fields(self, V_key):
        """Сложение полей A и B для слов, где V совпадает с V_key, записать результат в последние 5 бит."""
        results = []
        for j in range(self.size):
            word = self.get_word(j)
            V = self.extract_bits(word, 0, 2)
            if V == V_key:
                A = self.extract_bits(word, 3, 6)
                B = self.extract_bits(word, 7, 10)
                sum_AB = (A + B) & 0b11111
                word = self.set_bits(word, 11, 15, sum_AB)
                self.set_word(j, word)  # Записываем обратно в исходный столбец
                results.append((j, sum_AB, ''.join(str(bit) for bit in word)))
        return results