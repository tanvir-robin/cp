# -----------------------------
# Integer to Roman Numeral Translator
# -----------------------------
def int_to_roman(num):
    """
    Convert an integer (1-3999) to Roman numeral.
    """
    if not (0 < num < 4000):
        raise ValueError("Number must be between 1 and 3999")

    # Thousands
    M = ["", "M", "MM", "MMM"]
    # Hundreds
    H = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    # Tens
    T = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    # Units
    U = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

    # Syntax-directed translation: concatenate parts
    roman = (
        M[num // 1000]
        + H[(num % 1000) // 100]
        + T[(num % 100) // 10]
        + U[num % 10]
    )
    return roman


# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    examples = [3, 9, 58, 1994, 2023, 3999]
    for n in examples:
        print(f"{n} -> {int_to_roman(n)}")
