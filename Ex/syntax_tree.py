# -----------------------------
# Mini TAC Generator (Interactive)
# -----------------------------

temp = 1

def new_temp():
    """Generate new temporary variable."""
    global temp
    t = f"t{temp}"
    temp += 1
    return t

def tac(expr):
    """Generate three-address code for simple expressions with +, * and assignment."""
    global temp
    temp = 1

    # Remove spaces
    expr = expr.replace(" ", "")

    # Split assignment
    if '=' not in expr:
        print("Error: Expression must have '='")
        return
    var, right = expr.split('=')

    # ---- Handle '*' first ----
    plus_parts = right.split('+')
    temps = []
    for part in plus_parts:
        if '*' in part:
            a, b = part.split('*')
            t = new_temp()
            print(f"{t} = {a} * {b}")
            temps.append(t)
        else:
            temps.append(part)

    # ---- Handle '+' next ----
    result = temps[0]
    for t in temps[1:]:
        tmp = new_temp()
        print(f"{tmp} = {result} + {t}")
        result = tmp

    # ---- Final assignment ----
    print(f"{var} = {result}")

# ----- Interactive loop -----
print("Mini TAC Generator")
print("Type 'quit' to exit\n")

while True:
    expr = input("Expr: ").strip()
    if expr.lower() in ('quit', ''):
        break
    tac(expr)
    print()
