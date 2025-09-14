class Symbol:
    """Represents a symbol with a name and type."""
    def __init__(self, name, typ):
        self.name = name
        self.type = typ

    def __repr__(self):
        return f"Symbol(name='{self.name}', type='{self.type}')"

class SymbolTable:
    """Chain Symbol Table for nested scopes."""
    def __init__(self, parent=None):
        self.table = {}   # Dictionary for symbols in current scope
        self.parent = parent  # Link to parent scope (None if global)

    def insert(self, name, typ):
        """Insert a new symbol into the current scope."""
        if name in self.table:
            raise ValueError(f"Symbol '{name}' already declared in this scope")
        symbol = Symbol(name, typ)
        self.table[name] = symbol
        return symbol

    def lookup(self, name):
        """Lookup a symbol starting from current scope up the chain."""
        if name in self.table:
            return self.table[name]
        elif self.parent:
            return self.parent.lookup(name)
        else:
            return None

    def __repr__(self):
        return f"SymbolTable({self.table})"

# Example usage
if __name__ == "__main__":
    # Global scope
    global_scope = SymbolTable()
    global_scope.insert("x", "int")
    global_scope.insert("y", "float")

    # Function scope (child of global)
    func_scope = SymbolTable(parent=global_scope)
    func_scope.insert("z", "int")

    print("Global Scope:", global_scope)
    print("Function Scope:", func_scope)

    # Lookup examples
    print("Lookup x in function scope:", func_scope.lookup("x"))  # Should find in global
    print("Lookup z in global scope:", global_scope.lookup("z"))  # Should be None
