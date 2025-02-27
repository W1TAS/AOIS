from BinaryOperations import BinaryOperations

class IEEE754Operations:

    @staticmethod
    def binary_to_decimal(binary: str) -> int:
        decimal = 0
        for i, bit in enumerate(binary):
            decimal += int(bit) * (2 ** (len(binary) - 1 - i))
        return decimal

    @staticmethod
    def float_to_ieee754(num: float) -> str:
        sign = '1' if num < 0 else '0'
        num = abs(num)

        int_part = int(num)
        frac_part = num - int_part

        int_bin = ''
        if int_part == 0:
            int_bin = '0'
        else:
            while int_part > 0:
                int_bin = str(int_part % 2) + int_bin
                int_part //= 2

        frac_bin = []
        while frac_part > 0 and len(frac_bin) < 23:
            frac_part *= 2
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

        mantissa = (mantissa + '0' * 23)[:23]
        biased_exponent = exponent + 127

        exponent_bin = ''
        while biased_exponent > 0:
            exponent_bin = str(biased_exponent % 2) + exponent_bin
            biased_exponent //= 2

        exponent_bin = ('0' * 8 + exponent_bin)[-8:]

        return sign + exponent_bin + mantissa

    @staticmethod
    def ieee754_to_float(ieee754: str) -> float:
        sign = -1 if ieee754[0] == '1' else 1
        exponent = IEEE754Operations.binary_to_decimal(ieee754[1:9]) - 127
        mantissa_binary = ieee754[9:]

        mantissa = 1.0
        for i, bit in enumerate(mantissa_binary):
            if bit == '1':
                mantissa += 2 ** -(i + 1)

        return sign * mantissa * (2 ** exponent)

    @staticmethod
    def ieee754_to_binary_exp(ieee754_str):
        if len(ieee754_str) != 32 or not all(bit in '01' for bit in ieee754_str):
            raise ValueError("Некорректная строка формата IEEE754")

        # sign = ieee754_str[0]
        exponent_bits = ieee754_str[1:9]
        mantissa_bits = ieee754_str[9:]

        exponent = IEEE754Operations.binary_to_decimal(exponent_bits) - 127

        mantissa = '1' + mantissa_bits

        return mantissa, exponent

    @staticmethod
    def add_ieee754(mantissa1: str, exponent1: int, mantissa2: str, exponent2: int) -> str:
        # Выравнивание экспонент
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

        exponent_bits = IEEE754Operations.to_binary(exponent + 127).zfill(8)

        ieee754_result = '0' + exponent_bits + sum_mantissa[1:].ljust(23, '0')[:23]
        return ieee754_result

    @staticmethod
    def to_binary(value: int) -> str:
        binary = ''
        while value > 0:
            binary = str(value % 2) + binary
            value //= 2
        return binary
