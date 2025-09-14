# Sample tokens for demonstration
tokens = ["id", "+", "id", "-", "id"]
pos = 0

def next_token():
    global pos
    if pos < len(tokens):
        return tokens[pos]
    return None

def match(expected):
    global pos
    if next_token() == expected:
        pos += 1
    else:
        raise SyntaxError(f"Expected {expected}, got {next_token()}")

# Iterative term parser
def term():
    tok = next_token()
    if tok == "id" or tok.isdigit():
        match(tok)
    elif tok == "(":
        match("(")
        expr()
        match(")")
    else:
        raise SyntaxError(f"Unexpected token {tok}")

# Iterative expr parser eliminating tail recursion
def expr():
    term()  # parse first term

    # loop replaces recursive rest()
    while True:
        tok = next_token()
        if tok == "+":
            match("+")
            term()
        elif tok == "-":
            match("-")
            term()
        else:
            break  # epsilon

# Testing
try:
    expr()
    if pos == len(tokens):
        print("Parsing successful")
    else:
        print("Extra tokens remaining")
except SyntaxError as e:
    print(e)
