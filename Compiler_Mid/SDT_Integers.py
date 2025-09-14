# -----------------------------
# Roman Numerals to Integer (up to 2000)
# -----------------------------
def roman_to_int(roman):
    """
    Convert a Roman numeral (up to 2000) to an integer.
    """
    # Map of Roman symbols to values
    roman_map = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }

    total = 0
    i = 0
    while i < len(roman):
        # Check for subtractive pair
        if i + 1 < len(roman) and roman_map[roman[i]] < roman_map[roman[i+1]]:
            total += roman_map[roman[i+1]] - roman_map[roman[i]]
            i += 2
        else:
            total += roman_map[roman[i]]
            i += 1

    # Ensure value does not exceed 2000
    if total > 2000:
        raise ValueError("Roman numeral exceeds 2000")
    return total


# -----------------------------
# Examples
# -----------------------------
if __name__ == "__main__":
    examples = ["I", "IX", "LVIII", "M", "MM", "MCM"]
    for r in examples:
        value = roman_to_int(r)
        print(f"{r} -> {value}")
