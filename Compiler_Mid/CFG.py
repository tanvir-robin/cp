# Grammar:
# S -> S S + | S S * | a

class Node:
    """Parse tree node"""

    def __init__(self, symbol, children=None):
        self.symbol = symbol
        self.children = children if children else []

    def __repr__(self, level=0):
        ret = "  " * level + self.symbol + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret


def parse_postfix(tokens):
    """
    Parse a postfix expression into a parse tree.
    Works by using a stack (natural for postfix).
    """
    stack = []
    for tok in tokens:
        if tok == "a":
            stack.append(Node("S", [Node("a")]))
        elif tok in ["+", "*"]:
            # Pop two subtrees
            if len(stack) < 2:
                raise SyntaxError("Not enough operands for operator")
            right = stack.pop()
            left = stack.pop()
            stack.append(Node("S", [left, right, Node(tok)]))
        else:
            raise SyntaxError(f"Invalid token: {tok}")

    if len(stack) != 1:
        raise SyntaxError("Invalid postfix expression")

    return stack[0]


def build_parse_tree(expr):
    tokens = list(expr)  # split string into characters
    return parse_postfix(tokens)


# Example
if __name__ == "__main__":
    expr = "aa+a*"
    tree = build_parse_tree(expr)
    print("Parse tree for:", expr)
    print(tree)
