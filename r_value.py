# Symbol table
symbol_table = {}

# Evaluate rvalue
def rvalue(expr):
    if isinstance(expr, int):
        return expr
    elif isinstance(expr, str):
        return symbol_table.get(expr, 0)
    elif isinstance(expr, tuple):
        op, left, right = expr
        lval = rvalue(left)
        rval = rvalue(right)
        if op == '+': return lval + rval
        if op == '-': return lval - rval
        if op == '*': return lval * rval
        if op == '/': return lval / rval
    else:
        raise ValueError("Unknown expression type")

# Simple parser to convert string to tuples
def parse(expr_str):
    expr_str = expr_str.replace(" ", "")
    if "=" in expr_str:
        lhs, rhs = expr_str.split("=")
        return lhs, parse_expr(rhs)
    else:
        return parse_expr(expr_str)

def parse_expr(s):
    # Supports +, -, *, / (leftmost operator for simplicity)
    for op in ['+', '-', '*', '/']:
        if op in s:
            l, r = s.split(op, 1)
            lnode = int(l) if l.isdigit() else l
            rnode = int(r) if r.isdigit() else r
            return (op, lnode, rnode)
    return int(s) if s.isdigit() else s

# Example complex expressions
expressions = [
    "a = 5",
    "b = 10 + 2",
    "c = a + b * 2",
    "d = c - a / 5 + b * 3",
    "e = (a + b) * (c - d)"
]

# Evaluate and print results
for expr in expressions:
    lhs, rhs = parse(expr)
    val = rvalue(rhs)
    symbol_table[lhs] = val
    print(f"Input: {expr}  -->  rvalue: {lhs} = {val}")
