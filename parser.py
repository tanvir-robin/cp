# Super easy toy parser

def parse_statement(line):
    # Remove spaces and split tokens by simple rules
    tokens = []
    i = 0
    while i < len(line):
        if line[i].isspace():
            i += 1
        elif line[i] in "();":
            tokens.append(line[i])
            i += 1
        else:
            j = i
            while j < len(line) and line[j] not in " ();":
                j += 1
            tok = line[i:j]
            if tok not in {"expr", "if", "for", "other"}:
                print("Unknown token:", tok)
                return
            tokens.append(tok)
            i = j

    print("TOKENS:", tokens)

    # Very simple check: statement must start with expr/if/for/other
    if not tokens:
        print("Empty input")
        return

    first = tokens[0]
    if first in {"expr", "other"}:
        print("RESULT: OK")
    elif first == "if":
        if len(tokens) >= 5 and tokens[1]=="(" and tokens[2]=="expr" and tokens[3]==")" and tokens[4]=="expr":
            print("RESULT: OK")
        else:
            print("RESULT: Syntax error")
    elif first == "for":
        # Minimal check: at least 9 tokens: for ( expr ; expr ; expr ) expr
        if len(tokens) >= 9:
            print("RESULT: OK")
        else:
            print("RESULT: Syntax error")
    else:
        print("RESULT: Syntax error")

# --- Demo ---
line = input("Enter statement: ")
parse_statement(line)
