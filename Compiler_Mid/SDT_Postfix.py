# -----------------------------
# Postfix to Infix with Parse Tree
# -----------------------------
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value      # operator or number
        self.left = left        # left child (Node)
        self.right = right      # right child (Node)

    def infix(self):
        """Return infix expression with parentheses"""
        if self.left is None and self.right is None:
            return self.value
        return f"({self.left.infix()}{self.value}{self.right.infix()})"

    def print_tree(self, level=0):
        """Print parse tree in text format"""
        print("  " * level + str(self.value))
        if self.left:
            self.left.print_tree(level + 1)
        if self.right:
            self.right.print_tree(level + 1)


def postfix_to_infix(expr):
    """Convert postfix string to infix using a stack"""
    stack = []
    for tok in expr:
        if tok.isdigit():  # operand
            stack.append(Node(tok))
        elif tok in "+-*/":  # operator
            if len(stack) < 2:
                raise ValueError("Invalid postfix expression")
            right = stack.pop()
            left = stack.pop()
            stack.append(Node(tok, left, right))
        else:
            raise ValueError(f"Unknown token: {tok}")
    if len(stack) != 1:
        raise ValueError("Invalid postfix expression")
    return stack[0]  # root node


# -----------------------------
# Examples
# -----------------------------
if __name__ == "__main__":
    examples = ["95-2*", "952*-"]
    for ex in examples:
        root = postfix_to_infix(ex)
        print(f"Postfix: {ex}")
        print(f"Infix: {root.infix()}")
        print("Parse Tree:")
        root.print_tree()
        print("-" * 30)
