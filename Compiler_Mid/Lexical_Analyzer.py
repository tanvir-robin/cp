import re

# -----------------------------
# Function to remove comments
# -----------------------------


def remove_comments(code):
    """Remove single-line (// ...) and multi-line (/* ... */) comments"""
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)  # multi-line
    code = re.sub(r'//.*', '', code)                        # single-line
    return code

# -----------------------------
# Lexical Analyzer
# -----------------------------


def tokenize(code):
    """
    Tokenize code into identifiers, numbers, operators, relational/logical operators, punctuation
    """
    token_specification = [
        ('FLOAT', r'\d+\.\d*|\.\d+'),           # Floating-point numbers
        ('INT',   r'\d+'),                       # Integer numbers
        ('ID',    r'[A-Za-z_]\w*'),             # Identifiers
        ('RELOP', r'<=|>=|==|!=|<|>'),          # Relational operators
        ('LOGIC', r'&&|\|\|'),                  # Logical operators
        ('OP',    r'[+\-*/=]'),                 # Arithmetic operators
        ('PUNC',  r'[();{},]'),                 # Punctuation
        ('SKIP',  r'[ \t\n]+'),                 # Skip whitespace
        ('MISMATCH', r'.'),                      # Any other character
    ]

    tok_regex = '|'.join(
        f'(?P<{name}>{pattern})' for name, pattern in token_specification)
    tokens = []

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character: {value}')
        else:
            tokens.append((kind, value))

    return tokens


# -----------------------------
# Main execution
# -----------------------------
if __name__ == "__main__":
    code = """
    // Single-line comment
    int x = 3; /* multi-line
                  comment */
    float y = 3.14;
    if (x >= 2 && y < 4.5 || x != 0) {
        x = x + 1;
    }
    """

    print("Original Code:\n", code)
    clean_code = remove_comments(code)
    print("Code after removing comments:\n", clean_code)

    tokens = tokenize(clean_code)
    print("\nTokens:")
    for kind, value in tokens:
        print(f"{kind}: {value}")
