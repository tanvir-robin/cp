"""
Predictive Parser for the Grammar:
stmt -> expr; | if (expr) stmt | for(optexpr; optexpr) stmt | others
optexpr -> ε | expr
"""

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None
    
    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def read_identifier(self):
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result
    
    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char == ';':
                self.advance()
                return Token('SEMICOLON', ';')
            elif self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')
            elif self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')
            elif self.current_char.isalpha():
                identifier = self.read_identifier()
                if identifier in ['if', 'for', 'expr', 'others', 'test']:
                    return Token(identifier.upper(), identifier)
                else:
                    return Token('IDENTIFIER', identifier)
            else:
                raise Exception(f"Invalid character: {self.current_char}")
        
        return Token('EOF', None)

class PredictiveParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def error(self, message):
        raise Exception(f"Parse error: {message}")
    
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected {token_type}, got {self.current_token.type}")
    
    def parse_stmt(self):
        """
        Parse stmt -> expr; | if (expr) stmt | for(optexpr; optexpr) stmt | others
        """
        if self.current_token.type == 'EXPR':
            # stmt -> expr;
            self.eat('EXPR')
            self.eat('SEMICOLON')
            return "expr_statement"
        
        elif self.current_token.type == 'IF':
            # stmt -> if (expr) stmt
            self.eat('IF')
            self.eat('LPAREN')
            self.eat('EXPR')  # Parse expr
            self.eat('RPAREN')
            self.parse_stmt()  # Recursively parse nested stmt
            return "if_statement"
        
        elif self.current_token.type == 'FOR':
            # stmt -> for(optexpr; optexpr) stmt
            self.eat('FOR')
            self.eat('LPAREN')
            self.parse_optexpr()  # Parse first optexpr
            self.eat('SEMICOLON')
            self.parse_optexpr()  # Parse second optexpr
            self.eat('RPAREN')
            self.parse_stmt()  # Recursively parse nested stmt
            return "for_statement"
        
        elif self.current_token.type == 'OTHERS':
            # stmt -> others
            self.eat('OTHERS')
            return "other_statement"
        
        elif self.current_token.type == 'TEST':
            # Handle test command
            self.eat('TEST')
            return "test_command"
        
        else:
            self.error(f"Unexpected token: {self.current_token.type}")
    
    def parse_optexpr(self):
        """
        Parse optexpr -> ε | expr
        """
        if self.current_token.type == 'EXPR':
            # optexpr -> expr
            self.eat('EXPR')
            return "expression"
        else:
            # optexpr -> ε (empty)
            return "empty"

def parse(input_text):
    """
    Main parsing function
    """
    try:
        lexer = Lexer(input_text)
        parser = PredictiveParser(lexer)
        result = parser.parse_stmt()
        
        # Check if we've consumed all tokens
        if parser.current_token.type != 'EOF':
            raise Exception(f"Unexpected token after valid parse: {parser.current_token}")
        
        return True, result
    except Exception as e:
        return False, str(e)

def test_parser():
    """
    Test the predictive parser with various inputs
    """
    test_cases = [
        # Valid cases
        ("expr;", "expr_statement"),
        ("if (expr) expr;", "if_statement"),
        ("for(expr; expr) expr;", "for_statement"),
        ("for(; expr) expr;", "for_statement"),
        ("for(expr; ) expr;", "for_statement"),
        ("for(; ) expr;", "for_statement"),
        ("others", "other_statement"),
        ("if (expr) if (expr) expr;", "if_statement"),
        ("for(expr; expr) for(; expr) others", "for_statement"),
        
        # Invalid cases
        ("expr", "Missing semicolon"),
        ("if expr) expr;", "Missing opening parenthesis"),
        ("if (expr expr;", "Missing closing parenthesis"),
        ("for(expr; expr expr;", "Missing closing parenthesis"),
        ("unknown", "Unknown token"),
    ]
    
    print("Testing Predictive Parser")
    print("=" * 50)
    
    for i, (input_text, expected) in enumerate(test_cases, 1):
        print(f"\nTest {i}: {input_text}")
        success, result = parse(input_text)
        
        if success:
            print(f"✓ Valid: {result}")
        else:
            print(f"✗ Invalid: {result}")

if __name__ == "__main__":
    # Interactive mode
    print("Predictive Parser for the Grammar:")
    print("stmt -> expr; | if (expr) stmt | for(optexpr; optexpr) stmt | others")
    print("optexpr -> ε | expr")
    print("\nEnter 'test' to run test cases, or enter a statement to parse:")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() == 'test':
                test_parser()
            elif user_input.lower() in ['quit', 'exit', 'q']:
                break
            elif user_input:
                success, result = parse(user_input)
                if success:
                    print(f"✓ Valid statement: {result}")
                else:
                    print(f"✗ Parse error: {result}")
            else:
                print("Please enter a statement or 'test'")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
