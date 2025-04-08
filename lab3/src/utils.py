def glue_terms(term1, term2, variables="abc"):
    # Преобразуем термы в бинарный вид
    bin1 = ""
    bin2 = ""
    for var in variables:
        if f"¬{var}" in term1:
            bin1 += "0"
        elif var in term1:
            bin1 += "1"
        else:
            bin1 += "X"
        if f"¬{var}" in term2:
            bin2 += "0"
        elif var in term2:
            bin2 += "1"
        else:
            bin2 += "X"

    # Сравниваем бинарные строки
    diff = 0
    result_bin = ""
    for b1, b2 in zip(bin1, bin2):
        if b1 == b2:
            result_bin += b1
        else:
            diff += 1
            result_bin += "X"
        if diff > 1:
            return None

    if diff != 1:
        return None

    # Преобразуем обратно в строковый вид
    result = ""
    for i, val in enumerate(result_bin):
        if val == "1":
            result += variables[i]
        elif val == "0":
            result += f"¬{variables[i]}"
    return result

def print_table(table, orig_terms, imp_terms):
    print("Таблица покрытия:")
    header = "Импликанты | " + " | ".join(orig_terms)
    print(header)
    for imp in imp_terms:
        row = f"{imp:<10} | " + " | ".join("X" if t in table[imp] else " " for t in orig_terms)
        print(row)