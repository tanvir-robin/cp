# -----------------------------
# Recursive-Descent Parsers for 3 Grammars
# -----------------------------

# -----------------------------
# Grammar a: S -> + S S | - S S | a
# -----------------------------
def parse_a(expr, pos=0):
    if pos >= len(expr):
        return False, pos
    if expr[pos] == 'a':
        return True, pos + 1
    elif expr[pos] in '+-':
        ok1, next_pos1 = parse_a(expr, pos + 1)
        if not ok1:
            return False, pos
        ok2, next_pos2 = parse_a(expr, next_pos1)
        if not ok2:
            return False, pos
        return True, next_pos2
    else:
        return False, pos

# -----------------------------
# Grammar b: S -> S ( S ) S | ε
# -----------------------------


def parse_b(expr, pos=0):
    current = pos
    while current < len(expr) and expr[current] == '(':
        current += 1
        ok, current = parse_b(expr, current)
        if not ok:
            return False, pos
        if current >= len(expr) or expr[current] != ')':
            return False, pos
        current += 1
    return True, current

# -----------------------------
# Grammar c: S -> 0 S 1 | 0 1
# -----------------------------


def parse_c(expr, pos=0):
    if pos + 1 < len(expr) and expr[pos] == '0' and expr[pos + 1] == '1':
        return True, pos + 2
    elif pos < len(expr) and expr[pos] == '0':
        ok1, next_pos1 = parse_c(expr, pos + 1)
        if not ok1 or next_pos1 >= len(expr) or expr[next_pos1] != '1':
            return False, pos
        return True, next_pos1 + 1
    else:
        return False, pos


# -----------------------------
# Main execution
# -----------------------------
if __name__ == "__main__":
    examples = {
        'a': ["a", "+aa", "-+aaa", "++a-a a"],  # Grammar a
        'b': ["", "()", "(())", "()()", "(()())"],  # Grammar b
        'c': ["01", "0011", "000111", "0101", "001011"],  # Grammar c
    }

    for grammar, expr_list in examples.items():
        print(f"\nParsing examples for Grammar {grammar}:")
        for expr in expr_list:
            if grammar == 'a':
                success, next_pos = parse_a(expr)
            elif grammar == 'b':
                success, next_pos = parse_b(expr)
            elif grammar == 'c':
                success, next_pos = parse_c(expr)
            else:
                success = False
                next_pos = 0

            is_valid = success and next_pos == len(expr)
            print(
                f"Expression: {expr} -> {'Valid' if is_valid else 'Invalid'}")
