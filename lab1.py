

tokens = []   
pos = 0       


def peek():
    """Return current token without consuming it."""
    return tokens[pos] if pos < len(tokens) else None


def match(expected):
    """Consume a token if it matches, else raise error."""
    global pos
    if peek() == expected:
        pos += 1
    else:
        raise SyntaxError(f"Expected {expected}, got {peek()}")




def stmt():
    """stmt -> expr ; | if ( expr ) stmt | for ( optexpr ; optexpr ) stmt | others"""
    if peek() == "if":
        match("if")
        match("(")
        expr()
        match(")")
        stmt()
    elif peek() == "for":
        match("for")
        match("(")
        optexpr()
        match(";")
        optexpr()
        match(")")
        stmt()
    elif peek() == "others":
        match("others")
    else:
        expr()
        match(";")


def optexpr():
    """optexpr -> ε | expr"""
    if peek() in FIRST_EXPR():   
        expr()
    else:  
        pass


def expr():
    """Dummy expr parser: expr -> id | num"""
    if peek() == "id":
        match("id")
    elif peek() == "num":
        match("num")
    else:
        raise SyntaxError(f"Invalid expression start: {peek()}")


def FIRST_EXPR():
    """Tokens that can start an expression."""
    return {"id", "num"}



def parse(input_tokens):
    global tokens, pos
    tokens = input_tokens
    pos = 0
    stmt()
    if pos == len(tokens):
        print("Parsing successful")
    else:
        print("Parsing stopped at:", tokens[pos:])


if __name__ == "__main__":
    
    examples = [
        ["id", ";"],                                 
        ["if", "(", "id", ")", "others"],            
        ["for", "(", "id", ";", "num", ")", "others"],  
        ["for", "(", ";", ")", "others"],            
    ]

    for i, ex in enumerate(examples, 1):
        print(f"\nExample {i}: {ex}")
        try:
            parse(ex)
        except SyntaxError as e:
            print("Syntax error:", e)
