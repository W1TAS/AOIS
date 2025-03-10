class BinaryOperations:
    BIT_LENGTH_DEFAULT = 16
    FRACTIONAL_PRECISION = 5

    @staticmethod
    def int_to_binary(value: int, bit_length: int = BIT_LENGTH_DEFAULT) -> str:
        if value == 0:
            return '0'.zfill(bit_length - 1)
        binary = ''
        abs_value = abs(value)
        while abs_value > 0:
            binary = str(abs_value % 2) + binary
            abs_value //= 2
        return binary.zfill(bit_length - 1)

    @staticmethod
    def int_to_direct_code(value: int, bit_length: int = BIT_LENGTH_DEFAULT) -> str:
        sign = str(int(value < 0))
        return sign + BinaryOperations.int_to_binary(value, bit_length)

    @staticmethod
    def int_to_inverted_code(value: int, bit_length: int = BIT_LENGTH_DEFAULT) -> str:
        if value > 0:
            return BinaryOperations.int_to_direct_code(value, bit_length)
        inverted = '1' + ''.join('1' if bit == '0' else '0' for bit in BinaryOperations.int_to_direct_code(value, bit_length)[1:])
        return inverted

    @staticmethod
    def int_to_additional_code(value: int, bit_length: int = BIT_LENGTH_DEFAULT) -> str:
        if value >= 0:
            return BinaryOperations.int_to_direct_code(value, bit_length)
        inverted = list(BinaryOperations.int_to_inverted_code(value, bit_length))
        for i in range(len(inverted) - 1, 0, -1):
            if inverted[i] == '0':
                inverted[i] = '1'
                break
            else:
                inverted[i] = '0'
        return ''.join(inverted)

    @staticmethod
    def direct_to_decimal(binary: str) -> int:
        magnitude = 0
        for i, bit in enumerate(binary[1:]):
            magnitude += int(bit) * (2 ** (len(binary) - 2 - i))
        if binary[0] == '1':
            return -magnitude
        return magnitude

    @staticmethod
    def additional_to_decimal(binary: str) -> int:
        if binary[0] == '1':
            inverted = ''.join('1' if bit == '0' else '0' for bit in binary[1:])
            magnitude = BinaryOperations.direct_to_decimal('0' + inverted) + 1
            return -magnitude
        else:
            return BinaryOperations.direct_to_decimal(binary)

    @staticmethod
    def add_binary(bin1: str, bin2: str) -> str:
        max_len = max(len(bin1), len(bin2))
        bin1 = bin1.zfill(max_len)
        bin2 = bin2.zfill(max_len)
        result = []
        carry = 0
        for i in range(max_len - 1, -1, -1):
            bit1 = int(bin1[i])
            bit2 = int(bin2[i])
            total = bit1 + bit2 + carry
            result_bit = total % 2
            carry = total // 2
            result.append(str(result_bit))
        if carry:
            result.append('1')
        result = ''.join(reversed(result))
        return result

    @staticmethod
    def add_additional(bin1, bin2):
        max_len = max(len(bin1), len(bin2))
        bin1 = bin1.zfill(max_len)
        bin2 = bin2.zfill(max_len)

        carry = 0
        result = []

        for i in range(max_len - 1, -1, -1):
            bit1 = int(bin1[i])
            bit2 = int(bin2[i])

            total = bit1 + bit2 + carry
            result.append(str(total % 2))
            carry = total // 2

        if carry:
            result.append('1')

        result.reverse()
        result_str = ''.join(result)

        if len(result_str) > BinaryOperations.BIT_LENGTH_DEFAULT:
            result_str = result_str[1:]

        return result_str

    @staticmethod
    def binary_subtraction(bin1: str, bin2: str) -> str:
        inverted_b = ''.join('1' if bit == '0' else '0' for bit in bin2)
        additional_b = BinaryOperations.add_additional(inverted_b, '0' * (len(bin2) - 1) + '1')
        return BinaryOperations.add_additional(bin1, additional_b)

    @staticmethod
    def binary_multiplication(a: str, b: str) -> str:
        sign = '0' if a[0] == b[0] else '1'
        a = a[1:]
        b = b[1:]

        result_length = len(a)
        result = '0' * (result_length * 2)

        for i in range(len(b) - 1, -1, -1):
            if b[i] == '1':
                shifted = a + '0' * (len(b) - 1 - i)
                result = BinaryOperations.add_binary(result.zfill(len(shifted)), shifted.zfill(len(result)))

        return sign + result[-result_length:]

    @staticmethod
    def binary_subtraction_normal(bin1: str, bin2: str) -> str:
        max_len = max(len(bin1), len(bin2))
        bin1 = bin1.zfill(max_len)
        bin2 = bin2.zfill(max_len)

        result = []
        borrow = 0

        for i in range(max_len - 1, -1, -1):
            bit1 = int(bin1[i])
            bit2 = int(bin2[i])

            diff = bit1 - bit2 - borrow

            if diff < 0:
                diff += 2
                borrow = 1
            else:
                borrow = 0

            result.append(str(diff))

        result.reverse()
        return ''.join(result).lstrip('0') or '0'

    @staticmethod
    def binary_division(a: str, b: str, precision: int = FRACTIONAL_PRECISION) -> str:
        if b == '0' * len(b):
            raise ValueError("Деление на ноль невозможно")

        sign = '0' if a[0] == b[0] else '1'
        a = a[1:]
        b = b[1:]
        quotient = ''
        remainder = ''

        for bit in a:
            remainder += bit
            if int(remainder, 2) >= int(b, 2):
                quotient += '1'
                remainder = BinaryOperations.binary_subtraction_normal(remainder, b)
            else:
                quotient += '0'

        if not quotient:
            quotient = '0'

        quotient += '.'
        for _ in range(precision):
            remainder += '0'
            if int(remainder, 2) >= int(b, 2):
                quotient += '1'
                remainder = BinaryOperations.binary_subtraction_normal(remainder, b)
            else:
                quotient += '0'

        return sign + quotient

    @staticmethod
    def bin_frac_to_dec_frac(binary: str) -> float:
        sign = int(binary[0])
        if '.' in binary:
            integer_part, fractional_part = binary.split('.')
        else:
            integer_part = binary
            fractional_part = '0'

        integer_result = sum(int(bit) * (2 ** i) for i, bit in enumerate(reversed(integer_part[1:])))
        fractional_result = sum(int(bit) * (2 ** (-(i + 1))) for i, bit in enumerate(fractional_part))

        return (integer_result + fractional_result) * ((-1) ** sign)
