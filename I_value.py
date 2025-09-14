# Function to identify l-values in an expression
def find_lvalues(expr_str):
    expr_str = expr_str.replace(" ", "")
    lvalues = []
    if "=" in expr_str:
        lhs, rhs = expr_str.split("=")
        lvalues.append(lhs)  # left-hand side is always an l-value
    return lvalues

# Example input expressions
expressions = [
    "a = b + 5",
    "c = a * 2",
    "d = c - b",
    "x = y + z * 3"
]

# Print input and l-values
for expr in expressions:
    lvals = find_lvalues(expr)
    print(f"Input: {expr}")
    print(f"L-values: {', '.join(lvals)}\n")
