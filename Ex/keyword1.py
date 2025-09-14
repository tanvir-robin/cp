import keyword
import re

def identify_keywords_identifiers(code: str):
    """
    Identify keywords and identifiers from a given Python code string.
    """
    # Use regex to split code into words (letters, digits, and underscores)
    tokens = re.findall(r'\b\w+\b', code)

    for token in tokens:
        if keyword.iskeyword(token):
            print(f"'{token}': Keyword")
        elif token.isidentifier():
            print(f"'{token}': Identifier")
        else:
            print(f"'{token}': Invalid token")


# Main program with input code directly in the program
if __name__ == "__main__":
    code_input = """
def my_function(x, y):
    if x > y:
        return x
    else:
        return y

a = 10
b = 20
result = my_function(a, b)
print(result)
"""

    print("Input code:\n", code_input)
    print("\nScanning result for keywords and identifiers:\n")
    identify_keywords_identifiers(code_input)
