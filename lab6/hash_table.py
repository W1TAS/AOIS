# hash_table.py

class HashTable:
    def __init__(self, size=20):
        """Инициализация хеш-таблицы."""
        self.size = size  # Размер таблицы (H=20)
        self.occupied = 0  # Счетчик занятых ячеек
        # Структура ячейки: [ID, C, U, T, L, D, Po, Pi, V, h]
        self.cells = [
            {"ID": "", "C": 0, "U": 0, "T": 0, "L": 0, "D": 0, "Po": -1, "Pi": "", "V": -1, "h": -1}
            for _ in range(size)
        ]
        self.alphabet = {chr(ord('А') + i): i for i in range(33)}  # Русский алфавит: А=0, Б=1, ..., Я=32

    def calculate_V(self, key):
        """Вычисление числового значения ключа (V) по первым двум буквам."""
        if len(key) < 2:
            raise ValueError("Ключ должен содержать хотя бы 2 буквы")
        first, second = key[0].upper(), key[1].upper()
        if first not in self.alphabet or second not in self.alphabet:
            raise ValueError("Ключ содержит недопустимые символы")
        return self.alphabet[first] * 33 + self.alphabet[second]

    def calculate_hash(self, V):
        """Вычисление хеш-адреса (h)."""
        return V % self.size  # h = V mod H, B=0

    def quadratic_probe(self, h, attempt):
        """Квадратичный поиск для обработки коллизий."""
        # Примечание: квадратичный поиск может не покрывать все ячейки для H=20,
        # что является особенностью метода, а не ошибкой реализации.
        return (h + attempt ** 2) % self.size

    def insert(self, key, data):
        """Добавление новой записи в таблицу."""
        # Проверка на дубликат
        if self.search(key) is not None:
            raise ValueError(f"Ключ '{key}' уже существует")

        V = self.calculate_V(key)
        h = self.calculate_hash(V)
        attempt = 0
        current_h = h

        # Поиск свободной ячейки
        while self.cells[current_h]["U"] == 1:
            attempt += 1
            current_h = self.quadratic_probe(h, attempt)
            if attempt > self.size:
                raise ValueError("Таблица переполнена")

        # Запись в ячейку
        self.cells[current_h] = {
            "ID": key,
            "C": 1 if attempt > 0 else 0,  # Коллизия, если был пробинг
            "U": 1,  # Занято
            "T": 1,  # Конечная ячейка (Po=-1)
            "L": 0,  # Данные в Pi
            "D": 0,  # Не удалено
            "Po": -1,  # Указатель (пока не в цепочке)
            "Pi": data,
            "V": V,
            "h": current_h
        }
        self.occupied += 1

        # Обновление цепочки, если была коллизия
        if attempt > 0:
            prev_h = h
            prev_attempt = 0
            while self.cells[prev_h]["U"] == 1 and prev_attempt < attempt:
                if self.cells[prev_h]["Po"] == -1:
                    self.cells[prev_h]["Po"] = current_h
                    self.cells[prev_h]["T"] = 0  # Предыдущая ячейка больше не конечная
                    break
                prev_h = self.cells[prev_h]["Po"]
                prev_attempt += 1

    def search(self, key):
        """Поиск записи по ключу."""
        V = self.calculate_V(key)
        h = self.calculate_hash(V)
        attempt = 0
        current_h = h

        while self.cells[current_h]["U"] == 1:
            if self.cells[current_h]["ID"] == key and self.cells[current_h]["D"] == 0:
                return self.cells[current_h]["Pi"]
            if self.cells[current_h]["Po"] == -1:
                break
            current_h = self.cells[current_h]["Po"]
            attempt += 1
            if attempt > self.size:
                break
        return None

    def update(self, key, new_data):
        """Обновление данных для ключа."""
        V = self.calculate_V(key)
        h = self.calculate_hash(V)
        attempt = 0
        current_h = h

        while self.cells[current_h]["U"] == 1:
            if self.cells[current_h]["ID"] == key and self.cells[current_h]["D"] == 0:
                # Найдена активная ячейка с ключом, обновляем данные
                self.cells[current_h]["Pi"] = new_data
                return True
            if self.cells[current_h]["Po"] == -1:
                break  # Конец цепочки
            current_h = self.cells[current_h]["Po"]
            attempt += 1
            if attempt > self.size:
                break
        raise ValueError(f"Ключ '{key}' не найден")

    def delete(self, key):
        """Удаление записи по ключу."""
        V = self.calculate_V(key)
        h = self.calculate_hash(V)
        attempt = 0
        current_h = h
        prev_h = -1  # Индекс предыдущей ячейки в цепочке

        while self.cells[current_h]["U"] == 1:
            if self.cells[current_h]["ID"] == key and self.cells[current_h]["D"] == 0:
                # Найдена активная ячейка с ключом
                self.cells[current_h]["D"] = 1  # Помечаем как удаленную

                # Случай а: Одиночная ячейка (T=1, Po=-1)
                if self.cells[current_h]["T"] == 1 and self.cells[current_h]["Po"] == -1:
                    self.cells[current_h]["U"] = 0  # Освобождаем ячейку
                    self.occupied -= 1
                    return True

                # Случай б: Конечная ячейка в цепочке (T=1)
                if self.cells[current_h]["T"] == 1:
                    if prev_h != -1:
                        self.cells[prev_h]["T"] = 1  # Предыдущая становится конечной
                        self.cells[prev_h]["Po"] = -1
                    self.cells[current_h]["U"] = 0  # Освобождаем ячейку
                    self.occupied -= 1
                    return True

                # Случай в/г: Ячейка в середине или начале цепочки (T=0)
                next_h = self.cells[current_h]["Po"]
                if next_h != -1:
                    # Копируем следующую ячейку на место текущей
                    self.cells[current_h] = self.cells[next_h].copy()
                    self.cells[current_h]["h"] = current_h  # Обновляем h
                    self.cells[next_h]["U"] = 0  # Освобождаем следующую ячейку
                    self.cells[next_h]["D"] = 1
                    self.occupied -= 1
                    # Если скопированная ячейка была конечной, устанавливаем T=1
                    if self.cells[current_h]["Po"] == -1:
                        self.cells[current_h]["T"] = 1
                    return True
                else:
                    # Если Po=-1, но T=0 (не должно быть, но для безопасности)
                    self.cells[current_h]["U"] = 0
                    self.occupied -= 1
                    return True

            prev_h = current_h
            if self.cells[current_h]["Po"] == -1:
                break
            current_h = self.cells[current_h]["Po"]
            attempt += 1
            if attempt > self.size:
                break
        raise ValueError(f"Ключ '{key}' не найден")

    def get_fill_factor(self):
        """Коэффициент заполнения."""
        return self.occupied / self.size

    def print_table(self):
        """Вывод содержимого таблицы."""
        print(
            f"{'№':<3} {'ID':<15} {'C':<3} {'U':<3} {'T':<3} {'L':<3} {'D':<3} {'Po':<5} {'Pi':<30} {'V':<5} {'h':<5}"
        )
        print("-" * 80)
        for i, cell in enumerate(self.cells):
            if cell["U"] == 1 or cell["D"] == 1:  # Показываем удаленные ячейки для отладки
                print(
                    f"{i:<3} {cell['ID']:<15} {cell['C']:<3} {cell['U']:<3} {cell['T']:<3} {cell['L']:<3} {cell['D']:<3} {cell['Po']:<5} {cell['Pi']:<30} {cell['V']:<5} {cell['h']:<5}"
                )
        print(f"Коэффициент заполнения: {self.get_fill_factor():.2f}")