# --- Simple Token Classes ---

class Token:
    def __init__(self, tag):
        self.tag = tag
    def __str__(self):
        return f"Token<{self.tag}>"

class Num(Token):
    def __init__(self, value):
        super().__init__("NUM")
        self.value = value
    def __str__(self):
        return f"Num<{self.value}>"

class Word(Token):
    def __init__(self, tag, text):
        super().__init__(tag)
        self.text = text
    def __str__(self):
        return f"Word<{self.tag}, '{self.text}'>"

# --- Demo ---
if __name__ == "__main__":
    t1 = Token("+")
    t2 = Num(42)
    t3 = Word("ID", "x")

    print(t1)  # Token<+>
    print(t2)  # Num<42>
    print(t3)  # Word<ID, 'x'>
