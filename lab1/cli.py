import sys
from BinaryOperations import BinaryOperations
from IEEE754Operations import IEEE754Operations


def main():
    while True:
        print("\nВыберите действие:")
        print("1. Преобразование целых чисел в бинарные коды")
        print("2. Арифметические операции с целыми числами")
        print("3. Преобразование IEEE754")
        print("4. Арифметические операции с числами IEEE754")
        print("5. Выйти")

        choice = input("Введите номер действия: ")

        if choice == '1':
            value = int(input("Введите целое число: "))
            bit_length = int(input("Введите битовую длину (по умолчанию 16): ") or 16)
            print(f"Прямой код: {BinaryOperations.int_to_direct_code(value, bit_length)}")
            print(f"Обратный код: {BinaryOperations.int_to_inverted_code(value, bit_length)}")
            print(f"Дополнительный код: {BinaryOperations.int_to_additional_code(value, bit_length)}")

        elif choice == '2':
            a = int(input("Введите первое число: "))
            b = int(input("Введите второе число: "))
            a_bin = BinaryOperations.int_to_additional_code(a)
            b_bin = BinaryOperations.int_to_additional_code(b)

            print(a_bin)
            print(b_bin)

            add_res = BinaryOperations.add_additional(a_bin, b_bin)
            sub_res = BinaryOperations.binary_subtraction(a_bin, b_bin)
            print("Результат сложения:",add_res, BinaryOperations.additional_to_decimal(add_res))
            print("Результат вычитания:",sub_res, BinaryOperations.additional_to_decimal(sub_res))

            a_dir = BinaryOperations.int_to_direct_code(a)
            b_dir = BinaryOperations.int_to_direct_code(b)

            mult_res = BinaryOperations.binary_multiplication(a_dir, b_dir)
            div_res = BinaryOperations.binary_division(a_dir,b_dir, 5)

            print("Результат умножения", mult_res, BinaryOperations.direct_to_decimal(mult_res))
            print("Результат деления", div_res, BinaryOperations.bin_frac_to_dec_frac(div_res))

        elif choice == '3':
            ieee_str = input("Введите 32-битную строку в формате IEEE754: ")
            mantissa, exponent = IEEE754Operations.ieee754_to_binary_exp(ieee_str)
            print(f"Мантисса: {mantissa}")
            print(f"Экспонента: {exponent}")

        elif choice == '4':
            x = input("Введите первое число в формате IEEE754: ")
            y = input("Введите второе число в формате IEEE754: ")


            x_m, x_e = IEEE754Operations.ieee754_to_binary_exp(IEEE754Operations.float_to_ieee754(float(x)))
            y_m, y_e = IEEE754Operations.ieee754_to_binary_exp(IEEE754Operations.float_to_ieee754(float(y)))
            print("Результат сложения:", IEEE754Operations.add_ieee754(x_m, x_e, y_m, y_e))

            print(IEEE754Operations.ieee754_to_float(IEEE754Operations.add_ieee754(x_m, x_e, y_m, y_e)))
            # print(IEEE754Operations.)

        elif choice == '5':
            print("Выход из программы.")
            sys.exit()

        else:
            print("Некорректный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
