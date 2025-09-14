import re

# -----------------------------
# Tokenization
# -----------------------------


def tokenize(expr):
    # Split numbers, operators, parentheses
    return re.findall(r'\d+|[()+\-*/]', expr)


# -----------------------------
# Parser / SDTS for prefix translation
# -----------------------------
tokens = []
pos = 0


def peek():
    return tokens[pos] if pos < len(tokens) else None


def consume(expected=None):
    global pos
    tok = peek()
    if expected and tok != expected:
        raise SyntaxError(f"Expected {expected}, got {tok}")
    pos += 1
    return tok

# Factor → (E) | num


def parse_factor():
    tok = peek()
    if tok == "(":
        consume("(")
        result = parse_expr()
        consume(")")
        return result
    else:
        # Number literal
        consume()
        return tok

# Term → Term * Factor | Term / Factor | Factor


def parse_term():
    left = parse_factor()
    while peek() in ("*", "/"):
        op = consume()
        right = parse_factor()
        left = f"{op} {left} {right}"  # SDTS: prefix
    return left

# Expr → Expr + Term | Expr - Term | Term


def parse_expr():
    left = parse_term()
    while peek() in ("+", "-"):
        op = consume()
        right = parse_term()
        left = f"{op} {left} {right}"  # SDTS: prefix
    return left

# -----------------------------
# Main function
# -----------------------------


def infix_to_prefix(expr):
    global tokens, pos
    tokens = tokenize(expr)
    pos = 0
    prefix = parse_expr()
    if pos != len(tokens):
        raise SyntaxError("Unexpected token at end")
    return prefix


# -----------------------------
# Examples
# -----------------------------
if __name__ == "__main__":
    examples = ["9-5+2", "9-5*2", "(1+2)*3", "4*(5+6)-7"]
    for ex in examples:
        print(f"Infix: {ex} -> Prefix: {infix_to_prefix(ex)}")
