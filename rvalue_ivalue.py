# Super simple three-address code generator

temp_count = 1

def new_temp():
    global temp_count
    t = f"t{temp_count}"
    temp_count += 1
    return t

def emit(code_list, s):
    code_list.append(s)

# Evaluate an expression (simplified)
def rvalue(x, code_list):
    if isinstance(x, int):  # Constant
        return str(x)
    if isinstance(x, str):  # Variable
        return x
    if isinstance(x, tuple):  # ('op', left, right)
        op, left, right = x
        l = rvalue(left, code_list)
        r = rvalue(right, code_list)
        t = new_temp()
        emit(code_list, f"{t} = {l} {op} {r}")
        return t
    if isinstance(x, list):  # ['arr', array, index]
        arr, idx = x[1], x[2]
        idx_val = rvalue(idx, code_list)
        t = new_temp()
        emit(code_list, f"{t} = {arr}[{idx_val}]")
        return t

# Assignment
def assign(left, right, code_list):
    val = rvalue(right, code_list)
    if isinstance(left, str):
        emit(code_list, f"{left} = {val}")
    elif isinstance(left, list):  # array access
        arr, idx = left[1], left[2]
        idx_val = rvalue(idx, code_list)
        emit(code_list, f"{arr}[{idx_val}] = {val}")

# Demo examples
def demo():
    global temp_count
    examples = []

    # x = a + b * 3
    examples.append(('x', ('+', 'a', ('*', 'b', 3))))

    # x = (a + b) < (c - 1)
    examples.append(('x', ('<', ('+', 'a', 'b'), ('-', 'c', 1))))

    # a[i] = b + 2
    examples.append((['arr', 'a', 'i'], ('+', 'b', 2)))

    # x = a[i + 1] * c
    examples.append(('x', ('*', ['arr', 'a', ('+', 'i', 1)], 'c')))

    for idx, (left, right) in enumerate(examples, 1):
        temp_count = 1
        code_list = []
        assign(left, right, code_list)
        print(f"Demo {idx}:")
        print("\n".join(code_list))
        print()

if __name__ == "__main__":
    demo()
