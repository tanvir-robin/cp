class SyntaxTreeNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []

    def add_child(self, node):
        self.children.append(node)

    def __repr__(self):
        return f"SyntaxTreeNode({self.value!r}, {self.children!r})"

def print_syntax_tree(node, indent=0):
    print('  ' * indent + str(node.value))
    for child in node.children:
        print_syntax_tree(child, indent + 1)

# Example usage:
if __name__ == "__main__":
    root = SyntaxTreeNode("Expr")
    term = SyntaxTreeNode("Term")
    factor = SyntaxTreeNode("Factor", [SyntaxTreeNode("Number", [SyntaxTreeNode("42")])])
    term.add_child(factor)
    root.add_child(term)
    print_syntax_tree(root)