# main.py

from hash_table import HashTable
import os


def load_terms(file_path):
    """Загрузка биологических терминов из файла."""
    terms = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and ':' in line:
                    key, data = line.split(':', 1)
                    terms.append((key.strip(), data.strip()))
    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
    return terms


def demonstrate_hash_table():
    """Демонстрация работы хеш-таблицы."""
    # Инициализация хеш-таблицы
    table = HashTable(size=20)

    # Загрузка терминов
    terms_file = os.path.join("data", "biology_terms.txt")
    terms = load_terms(terms_file)

    print("=== Вставка терминов ===")
    for key, data in terms:
        try:
            print(f"\nВставка: {key}")
            table.insert(key, data)
            table.print_table()
        except ValueError as e:
            print(f"Ошибка: {e}")

    print("\n=== Поиск терминов ===")
    test_keys = ["митоз", "микроб", "геном", "несуществующий"]
    for key in test_keys:
        result = table.search(key)
        print(f"Поиск '{key}': {result if result else 'Не найден'}")

    print("\n=== Обновление терминов ===")
    updates = [
        ("микроб", "бактерия или вирус"),
        ("геном", "полный набор ДНК организма")
    ]
    for key, new_data in updates:
        try:
            print(f"\nОбновление: {key}")
            table.update(key, new_data)
            table.print_table()
        except ValueError as e:
            print(f"Ошибка: {e}")

    print("\n=== Удаление терминов ===")
    delete_keys = ["митоз", "мицелий"]
    for key in delete_keys:
        try:
            print(f"\nУдаление: {key}")
            table.delete(key)
            table.print_table()
        except ValueError as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    demonstrate_hash_table()