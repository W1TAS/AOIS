from src.matrix import Matrix

class MatrixInterface:
    def __init__(self):
        """Инициализация интерфейса."""
        self.matrix = None

    def create_matrix(self, size=16):
        """Создать матрицу заданного размера."""
        self.matrix = Matrix(size)
        print(f"Матрица {size}x{size} создана.")
        self.view_matrix()

    def view_matrix(self):
        """Просмотреть матрицу."""
        if self.matrix is None:
            print("Ошибка: матрица не создана. Используйте команду 'create <size>'.")
            return
        self.matrix.display_matrix()

    def view_word(self, col):
        """Вывести слово по индексу столбца."""
        if self.matrix is None:
            print("Ошибка: матрица не создана. Используйте команду 'create <size>'.")
            return
        print(self.matrix.display_word(col))

    def perform_logical_operation(self, func_id, col1, col2, target_col):
        """Выполнить логическую операцию (f0, f5, f10, f15) над словами из столбцов col1 и col2, записать в target_col."""
        if self.matrix is None:
            print("Ошибка: матрица не создана. Используйте команду 'create <size>'.")
            return
        if func_id not in [0, 5, 10, 15]:
            print("Ошибка: доступны только функции f0, f5, f10, f15.")
            return
        result = self.matrix.logical_operation(func_id, col1, col2, target_col)
        print(result)
        self.view_matrix()

    def perform_addition(self, V_key):
        """Выполнить сложение Aj и Bj для слов с заданным V, записать результат в последние 5 бит."""
        if self.matrix is None:
            print("Ошибка: матрица не создана. Используйте команду 'create <size>'.")
            return
        results = self.matrix.add_fields(V_key)
        if not results:
            print(f"Слов с V={bin(V_key)[2:].zfill(3)} не найдено.")
        for j, sum_AB, word in results:
            print(f"Слово {j}: Aj + Bj = {sum_AB}, Новое слово: {word}")
        self.view_matrix()

    def search_by_match(self, argument):
        """Выполнить поиск по соответствию с заданным аргументом."""
        if self.matrix is None:
            print("Ошибка: матрица не создана. Используйте команду 'create <size>'.")
            return
        matching_words, max_matches = self.matrix.search_by_match(argument)
        print(f"Поиск по соответствию с аргументом {bin(argument)[2:].zfill(16)}:")
        print(f"Максимальное число совпадений: {max_matches}")
        print("Подходящие слова (столбцы):", matching_words)

    def cli(self):
        """Командная строка для взаимодействия с матрицей."""
        print("Добро пожаловать в CLI для работы с матрицей!")
        print("Доступные команды:")
        print("  create <size>       - Создать матрицу заданного размера (по умолчанию 16)")
        print("  view                - Просмотреть матрицу")
        print("  view_word <col>     - Вывести слово по индексу столбца")
        print("  logic <func_id> <col1> <col2> <target_col> - Выполнить логическую операцию (f0, f5, f10, f15)")
        print("  add <V_key>         - Сложить Aj и Bj для слов с заданным V (V в двоичном виде, например 111)")
        print("  search <argument>   - Поиск по соответствию (аргумент в двоичном виде)")
        print("  exit                - Выйти из программы")

        while True:
            command = input("Введите команду: ").strip().split()
            if not command:
                continue

            cmd = command[0].lower()
            if cmd == "create":
                size = int(command[1]) if len(command) > 1 else 16
                self.create_matrix(size)
            elif cmd == "view":
                self.view_matrix()
            elif cmd == "view_word" and len(command) == 2:
                self.view_word(int(command[1]))
            elif cmd == "logic" and len(command) == 5:
                self.perform_logical_operation(int(command[1]), int(command[2]), int(command[3]), int(command[4]))
            elif cmd == "add" and len(command) == 2:
                V_key = int(command[1], 2) if command[1].startswith('0b') else int(command[1], 2)
                self.perform_addition(V_key)
            elif cmd == "search" and len(command) == 2:
                argument = int(command[1], 2) if command[1].startswith('0b') else int(command[1], 2)
                self.search_by_match(argument)
            elif cmd == "exit":
                print("Выход из программы.")
                break
            else:
                print("Неверная команда. Введите 'help' для списка команд.")

if __name__ == "__main__":
    interface = MatrixInterface()
    interface.cli()