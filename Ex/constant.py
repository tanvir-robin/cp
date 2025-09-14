def scan_integer_constant(source_code: str, start_pos: int):
    """
    Scan an integer constant starting from start_pos in source_code.
    Returns:
        value: the integer value of the constant
        next_pos: position after the constant
    """
    i = start_pos
    v = 0

    # Show the input string being scanned
    print(f"Input to scan: '{source_code[i:]}'")

    # Scan digits to form the integer
    while i < len(source_code) and source_code[i].isdigit():
        v = v * 10 + int(source_code[i])
        i += 1

    print(f"Integer scanned: {v}, ends at pos {i}")
    return v, i


# Example usage
if __name__ == "__main__":
    code = "   12345 + 67"

    # Skip initial whitespace
    pos = 0
    while pos < len(code) and code[pos] in [' ', '\t', '\n']:
        pos += 1

    print(f"Original input: '{code}'\n")
    value, next_pos = scan_integer_constant(code, pos)
    print(f"\nResult: Value = {value}, Next scanning position = {next_pos}")
