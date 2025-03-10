from lab1.classes.BinaryOperations import BinaryOperations

# Константы
IEEE754_ZERO = '00000000000000000000000000000000'
IEEE754_SIGNIFICAND_LENGTH = 23
IEEE754_EXPONENT_LENGTH = 8
IEEE754_BIAS = 127
IEEE754_TOTAL_BITS = 32
IEEE754_DENORMALIZED_EXPONENT = -127
IEEE754_HIDDEN_BIT = '1'
BINARY_BASE = 2


class IEEE754Operations:

    @staticmethod
    def binary_to_decimal(binary: str) -> int:
        decimal = 0
        for i, bit in enumerate(binary):
            decimal += int(bit) * (BINARY_BASE ** (len(binary) - 1 - i))
        return decimal

    @staticmethod
    def float_to_ieee754(num: float) -> str:
        if num == 0:
            return IEEE754_ZERO
        else:
            sign = '1' if num < 0 else '0'
            num = abs(num)

            int_part = int(num)
            frac_part = num - int_part

            int_bin = ''
            if int_part == 0:
                int_bin = '0'
            else:
                while int_part > 0:
                    int_bin = str(int_part % BINARY_BASE) + int_bin
                    int_part //= BINARY_BASE

            frac_bin = []
            while frac_part > 0 and len(frac_bin) < IEEE754_SIGNIFICAND_LENGTH:
                frac_part *= BINARY_BASE
                bit = int(frac_part)
                frac_bin.append(str(bit))
                frac_part -= bit

            if int_bin != '0':
                exponent = len(int_bin) - 1
                mantissa = int_bin[1:] + ''.join(frac_bin)
            else:
                first_one_index = ''.join(frac_bin).find('1')
                exponent = -(first_one_index + 1)
                mantissa = ''.join(frac_bin)[first_one_index + 1:]

            mantissa = (mantissa + '0' * IEEE754_SIGNIFICAND_LENGTH)[:IEEE754_SIGNIFICAND_LENGTH]
            biased_exponent = exponent + IEEE754_BIAS

            exponent_bin = ''
            while biased_exponent > 0:
                exponent_bin = str(biased_exponent % BINARY_BASE) + exponent_bin
                biased_exponent //= BINARY_BASE

            exponent_bin = ('0' * IEEE754_EXPONENT_LENGTH + exponent_bin)[-IEEE754_EXPONENT_LENGTH:]

            return sign + exponent_bin + mantissa

    @staticmethod
    def ieee754_to_float(ieee754: str) -> float:
        if ieee754 == IEEE754_ZERO:
            return 0.0
        else:
            sign = -1 if ieee754[0] == '1' else 1
            exponent = IEEE754Operations.binary_to_decimal(ieee754[1:9]) - IEEE754_BIAS
            mantissa_binary = ieee754[9:]

            mantissa = 1.0
            for i, bit in enumerate(mantissa_binary):
                if bit == '1':
                    mantissa += BINARY_BASE ** -(i + 1)

            return sign * mantissa * (BINARY_BASE ** exponent)

    @staticmethod
    def ieee754_to_binary_exp(ieee754_str):
        if len(ieee754_str) != IEEE754_TOTAL_BITS or not all(bit in '01' for bit in ieee754_str):
            raise ValueError("Некорректная строка формата IEEE754")

        exponent_bits = ieee754_str[1:9]
        mantissa_bits = ieee754_str[9:]

        exponent = IEEE754Operations.binary_to_decimal(exponent_bits) - IEEE754_BIAS
        mantissa = IEEE754_HIDDEN_BIT + mantissa_bits

        return mantissa, exponent

    @staticmethod
    def add_ieee754(mantissa1: str, exponent1: int, mantissa2: str, exponent2: int) -> str:
        if mantissa1 == mantissa2 == '100000000000000000000000' and exponent1 == exponent2 == IEEE754_DENORMALIZED_EXPONENT:
            return IEEE754_ZERO
        else:
            if exponent1 > exponent2:
                shift = exponent1 - exponent2
                mantissa2 = '0' * shift + mantissa2
                mantissa1 += '0' * shift
                exponent = exponent1
            else:
                shift = exponent2 - exponent1
                mantissa1 = '0' * shift + mantissa1
                mantissa2 += '0' * shift
                exponent = exponent2

            sum_mantissa = BinaryOperations.add_binary(mantissa1, mantissa2)

            if len(sum_mantissa) > len(mantissa1):
                exponent += 1

            exponent_bits = IEEE754Operations.to_binary(exponent + IEEE754_BIAS).zfill(IEEE754_EXPONENT_LENGTH)

            ieee754_result = '0' + exponent_bits + sum_mantissa[1:].ljust(IEEE754_SIGNIFICAND_LENGTH, '0')[:IEEE754_SIGNIFICAND_LENGTH]
            return ieee754_result

    @staticmethod
    def to_binary(value: int) -> str:
        binary = ''
        while value > 0:
            binary = str(value % BINARY_BASE) + binary
            value //= BINARY_BASE
        return binary
