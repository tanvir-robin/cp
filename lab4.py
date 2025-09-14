def remove_whitespace(code: str) -> str:
    # Remove spaces, tabs, and newlines
    cleaned_code = "".join(code.split())
    return cleaned_code


source_code = """
int main() {
    int a = 5;   // variable
    int b = 10;  
    return a + b;   
}
"""

print("Original Code:\n", source_code)
print("\nCode Without Whitespace:\n", remove_whitespace(source_code))
