import re

def lexer(code):
    # Token patterns
    token_spec = [
        ("NUM",   r'\d+'),              # Numbers
        ("ID",    r'[A-Za-z_]\w*'),     # Identifiers
        ("OP",    r'[+\-*/=()]'),       # Operators & parens
        ("SKIP",  r'[ \t]+'),           # Skip spaces/tabs
        ("NEWLINE", r'\n'),             # Newlines
    ]
    tok_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec)

    tokens = []
    for match in re.finditer(tok_regex, code):
        kind = match.lastgroup
        value = match.group()

        if kind == "NUM":
            tokens.append(("NUM", value))
        elif kind == "ID":
            if value in ("true", "false"):
                tokens.append(("BOOL", value))
            else:
                tokens.append(("ID", value))
        elif kind == "OP":
            tokens.append(("OP", value))
        elif kind == "NEWLINE":
            tokens.append(("NEWLINE", "\\n"))
        # SKIP = ignore
    return tokens


# ----- Demo -----
source = """true false
x1 123 ; ( ) + - *
y99
"""
print("SOURCE:")
print(source)
print("\nTOKENS:")
for t in lexer(source):
    print(t)
