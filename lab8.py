class Node:
    def __init__(self, kind, value=None, children=None):
        self.kind = kind
        self.value = value
        self.children = children or []

    def __repr__(self):
        if self.value:
            return f"{self.kind}({self.value})"
        return f"{self.kind}({self.children})"


class InstructionGenerator:
    def __init__(self):
        self.temp_count = 0
        self.instructions = []

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def rvalue(self, x):
        # If x is already an identifier or constant
        if isinstance(x, Node) and x.kind in ("IDENT", "CONST"):
            return x

        # Otherwise, generate a temporary to hold the value
        t = self.new_temp()
        temp_node = Node("IDENT", t)
        self.instructions.append(f"{t} = Id({x})")
        return temp_node

    def lvalue(self, x):
        # For simplicity, lvalue just calls rvalue
        return self.rvalue(x)


# Example usage:
if __name__ == "__main__":
    gen = InstructionGenerator()

    # Example nodes
    x = Node("IDENT", "x")
    five = Node("CONST", "5")
    expr = Node("ADD", children=[x, five])   # (x + 5)

    # Generate rvalue
    rv = gen.rvalue(expr)

    print("Result node:", rv)
    print("Instructions:")
    for ins in gen.instructions:
        print("  ", ins)
