# -----------------------------
# Postfix to Prefix Translator
# -----------------------------

import re


def tokenize(expr):
    """
    Tokenize the expression into numbers, variables, and operators.
    Handles spaces correctly.
    """
    # Match multi-digit numbers, letters (variables), or single operators
    return re.findall(r'\d+|[a-zA-Z]+|[+\-*/]', expr)


def postfix_to_prefix(expr):
    """
    Convert a postfix expression string to prefix notation.
    """
    tokens = tokenize(expr)
    stack = []
    operators = set("+-*/")

    for tok in tokens:
        if tok not in operators:
            # Operand (number or variable)
            stack.append(tok)
        else:
            # Operator: pop two operands
            if len(stack) < 2:
                raise ValueError(f"Invalid postfix expression: {expr}")
            right = stack.pop()
            left = stack.pop()
            stack.append(f"{tok} {left} {right}")

    if len(stack) != 1:
        raise ValueError(f"Invalid postfix expression: {expr}")

    return stack[0]


# -----------------------------
# Main execution
# -----------------------------
if __name__ == "__main__":
    examples = [
        "9 5 - 2 *",
        "9 5 2 * -",
        "2 3 + 4 *",
        "x y + z *",
        "12 3 4 + *"  # multi-digit number example
    ]

    for expr in examples:
        prefix = postfix_to_prefix(expr)
        print(f"Postfix: {expr} -> Prefix: {prefix}")
