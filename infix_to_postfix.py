import re

def infix_to_postfix(expr):
    precedence = {'+':1, '-':1, '*':2, '/':2}
    stack = []
    output = []

    # Remove spaces
    expr = expr.replace(" ", "")
    # Tokenize numbers and operators
    tokens = re.findall(r'\d+|[()+\-*/]', expr)

    for token in tokens:
        if token.isdigit():
            output.append(token)
        elif token in '+-*/':
            while stack and stack[-1] != '(' and precedence.get(stack[-1],0) >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # remove '('

    while stack:
        output.append(stack.pop())

    print('Postfix:', ' '.join(output))


# Interactive mode
print("Enter 'quit' to exit")
while True:
    expr = input("Infix expression: ").strip()
    if expr.lower() in ['quit', '']:
        break
    infix_to_postfix(expr)
