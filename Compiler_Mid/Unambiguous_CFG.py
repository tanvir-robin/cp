import random
import re

# =========================
# (a) Postfix Expressions
# =========================

ops = ["+", "-", "*", "/"]
ids = ["x", "y", "z"]
ints = ["1", "2", "3"]


def gen_postfix(depth=2):
    """Generate a random postfix expression using the CFG:
       E → id | int | E E op"""
    if depth == 0:
        return random.choice(ids + ints)
    else:
        left = gen_postfix(depth - 1)
        right = gen_postfix(depth - 1)
        op = random.choice(ops)
        return f"{left} {right} {op}"


# ======================================
# (b) Left-associative identifier lists
# ======================================

def gen_left_list(n=3):
    """Generate left-associative lists: L → L , id | id"""
    result = "id1"
    for i in range(2, n + 1):
        result = f"{result}, id{i}"
    return result


# =======================================
# (c) Right-associative identifier lists
# =======================================

def gen_right_list(n=3, start=1):
    """Generate right-associative lists: L → id , L | id"""
    if n == 1:
        return f"id{start}"
    return f"id{start}, {gen_right_list(n - 1, start + 1)}"


# ========================================================
# (d) Arithmetic expressions with precedence & associativity
# ========================================================

tokens = []
pos = 0


def tokenize(expr):
    return re.findall(r"\d+|[a-zA-Z_]\w*|[()+\-*/]", expr)


def peek():
    global pos
    return tokens[pos] if pos < len(tokens) else None


def consume(expected=None):
    global pos
    tok = peek()
    if expected and tok != expected:
        raise SyntaxError(f"Expected {expected}, got {tok}")
    pos += 1
    return tok


def parse_expr():
    node = parse_term()
    while peek() in ("+", "-"):
        op = consume()
        right = parse_term()
        node = ("binop", op, node, right)
    return node


def parse_term():
    node = parse_factor()
    while peek() in ("*", "/"):
        op = consume()
        right = parse_factor()
        node = ("binop", op, node, right)
    return node


def parse_factor():
    tok = peek()
    if tok == "(":
        consume("(")
        node = parse_expr()
        consume(")")
        return node
    elif tok.isdigit():
        return ("int", consume())
    else:
        return ("id", consume())


def parse_arithmetic(expr):
    """Parse arithmetic expression with +,-,*,/ and precedence rules"""
    global tokens, pos
    tokens = tokenize(expr)
    pos = 0
    tree = parse_expr()
    if pos != len(tokens):
        raise SyntaxError("Unexpected input at end")
    return tree


# =========================
# Demo / Test
# =========================
if __name__ == "__main__":
    print("=== (a) Postfix Expressions ===")
    for _ in range(3):
        print(gen_postfix(2))

    print("\n=== (b) Left-associative Lists ===")
    print(gen_left_list(3))   # (id1, id2), id3
    print(gen_left_list(5))

    print("\n=== (c) Right-associative Lists ===")
    print(gen_right_list(3))  # id1, (id2, id3)
    print(gen_right_list(5))

    print("\n=== (d) Arithmetic Expression Parser ===")
    examples = ["a + b * c", "(a - b) / 3", "x * y - z / 2"]
    for ex in examples:
        print(ex, "=>", parse_arithmetic(ex))
