"""
lab6.py

A complete, self-contained lexical analyzer (lexer/tokenizer) in Python.
Features:
- Token dataclass with type, value, line, column
- Recognizes keywords, identifiers, integers, floats, strings (with escapes),
  operators, delimiters, comments (single and multi-line), and whitespace handling
- Good error messages with line/column info
- Lexer.tokenize() returns a list of tokens; Lexer is also iterable
- Example usage in __main__ demonstrating tokenization of a sample input

This is language-agnostic but inspired by C/Java/Python-style tokens. Adjust
KEYWORDS / OPERATORS / DELIMITERS to match the target language.
"""

from dataclasses import dataclass
from typing import List, Optional, Iterator
import re


@dataclass
class Token:
    type: str
    value: Optional[str]
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value!r}, {self.line}:{self.column})"


class LexicalError(Exception):
    pass


class Lexer:
    # Customize these sets as needed for a specific language
    KEYWORDS = {
        'if', 'else', 'for', 'while', 'return', 'break', 'continue', 'class', 'def', 'import', 'from', 'as',
        'pass', 'in', 'and', 'or', 'not', 'True', 'False', 'None', 'int', 'float', 'char', 'void', 'new'
    }

    OPERATORS = {
        '==', '!=', '<=', '>=', '+=', '-=', '*=', '/=', '++', '--', '&&', '||', '<<', '>>',
        '+', '-', '*', '/', '%', '<', '>', '=', '!', '&', '|', '^', '~', '?', ':'
    }

    DELIMITERS = {
        '(', ')', '{', '}', '[', ']', ',', ';', '.', '@'
    }

    # regex pieces for numbers/identifiers
    _identifier_re = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')
    _int_re = re.compile(r'\d+')
    _float_re = re.compile(r'(?:\d+\.\d*|\.\d+)(?:[eE][+-]?\d+)?')
    _number_with_exp_re = re.compile(r'\d+[eE][+-]?\d+')

    def __init__(self, source: str):
        self.source = source
        self.length = len(source)
        self.pos = 0
        self.line = 1
        self.col = 1

    def _peek(self, offset: int = 0) -> Optional[str]:
        i = self.pos + offset
        if i >= self.length:
            return None
        return self.source[i]

    def _advance(self, n: int = 1) -> str:
        chars = self.source[self.pos:self.pos+n]
        for ch in chars:
            if ch == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1
        self.pos += n
        return chars

    def _match(self, text: str) -> bool:
        if self.source.startswith(text, self.pos):
            self._advance(len(text))
            return True
        return False

    def _skip_whitespace_and_comments(self) -> None:
        while True:
            ch = self._peek()
            if ch is None:
                return
            # whitespace
            if ch.isspace():
                self._advance()
                continue
            # single-line comment: // ... or # ...
            if self._peek() == '/' and self._peek(1) == '/':
                # skip to end of line
                self._advance(2)
                while self._peek() not in (None, '\n'):
                    self._advance()
                continue
            if self._peek() == '#' :
                # Python-style comment to end of line
                self._advance()
                while self._peek() not in (None, '\n'):
                    self._advance()
                continue
            # multi-line comment /* ... */
            if self._peek() == '/' and self._peek(1) == '*':
                self._advance(2)
                while not (self._peek() == '*' and self._peek(1) == '/'):
                    if self._peek() is None:
                        raise LexicalError(f"Unterminated comment at line {self.line} col {self.col}")
                    self._advance()
                self._advance(2)
                continue
            break

    def _read_string(self) -> Token:
        quote = self._peek()
        assert quote in ('"', "'")
        start_line, start_col = self.line, self.col
        self._advance()  # skip opening quote
        value_chars = []
        while True:
            ch = self._peek()
            if ch is None:
                raise LexicalError(f"Unterminated string literal starting at {start_line}:{start_col}")
            if ch == '\\':
                # escape sequence
                self._advance()
                esc = self._peek()
                if esc is None:
                    raise LexicalError(f"Invalid escape at end of file in string starting at {start_line}:{start_col}")
                # simple escapes
                escapes = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', "'": "'"}
                if esc in escapes:
                    value_chars.append(escapes[esc])
                    self._advance()
                elif esc == 'u':
                    # unicode escape \uXXXX
                    self._advance()
                    hex_digits = ''
                    for _ in range(4):
                        d = self._peek()
                        if d is None or not re.match(r'[0-9a-fA-F]', d):
                            raise LexicalError(f"Invalid unicode escape in string at {self.line}:{self.col}")
                        hex_digits += d
                        self._advance()
                    value_chars.append(chr(int(hex_digits, 16)))
                else:
                    # unknown escape -> keep literal
                    value_chars.append(esc)
                    self._advance()
                continue
            if ch == quote:
                self._advance()  # consume closing
                break
            # normal char
            value_chars.append(ch)
            self._advance()
        return Token('STRING', ''.join(value_chars), start_line, start_col)

    def _read_number(self) -> Token:
        start_line, start_col = self.line, self.col
        s = self.source[self.pos:]
        # try float with decimal part
        m = self._float_re.match(s)
        if m:
            text = m.group(0)
            self._advance(len(text))
            return Token('NUMBER', text, start_line, start_col)
        # try integer with exponent
        m = self._number_with_exp_re.match(s)
        if m:
            text = m.group(0)
            self._advance(len(text))
            return Token('NUMBER', text, start_line, start_col)
        # try integer
        m = self._int_re.match(s)
        if m:
            text = m.group(0)
            self._advance(len(text))
            return Token('NUMBER', text, start_line, start_col)
        # fallback -- should not happen
        raise LexicalError(f"Invalid numeric literal at {start_line}:{start_col}")

    def _read_identifier_or_keyword(self) -> Token:
        start_line, start_col = self.line, self.col
        s = self.source[self.pos:]
        m = self._identifier_re.match(s)
        if not m:
            raise LexicalError(f"Invalid identifier start at {start_line}:{start_col}")
        text = m.group(0)
        self._advance(len(text))
        if text in self.KEYWORDS:
            return Token('KEYWORD', text, start_line, start_col)
        return Token('IDENT', text, start_line, start_col)

    def _read_operator_or_delimiter(self) -> Token:
        start_line, start_col = self.line, self.col
        # Try longest match for operators (two-char operators first)
        two = None
        if self._peek(0) and self._peek(1):
            two = self._peek(0) + self._peek(1)
        if two and two in self.OPERATORS:
            self._advance(2)
            return Token('OP', two, start_line, start_col)
        ch = self._peek()
        if ch in self.OPERATORS:
            self._advance()
            return Token('OP', ch, start_line, start_col)
        if ch in self.DELIMITERS:
            self._advance()
            return Token('DELIM', ch, start_line, start_col)
        # unknown single-char token
        self._advance()
        return Token('UNKNOWN', ch, start_line, start_col)

    def next_token(self) -> Optional[Token]:
        self._skip_whitespace_and_comments()
        ch = self._peek()
        if ch is None:
            return None

        # strings
        if ch in ('"', "'"):
            return self._read_string()

        # numbers
        if ch.isdigit() or (ch == '.' and self._peek(1) and self._peek(1).isdigit()):
            return self._read_number()

        # identifier or keyword
        if ch.isalpha() or ch == '_':
            return self._read_identifier_or_keyword()

        # operator/delimiter
        return self._read_operator_or_delimiter()

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        while True:
            tok = self.next_token()
            if tok is None:
                break
            tokens.append(tok)
        return tokens

    # make lexer iterable
    def __iter__(self) -> Iterator[Token]:
        while True:
            t = self.next_token()
            if t is None:
                break
            yield t


if __name__ == '__main__':
    sample = r'''
    // sample program
    int main() {
        float x = 3.14;
        int y = 42;
        string s = "Hello, \"world\"\\n";
        /* multi-line
           comment */
        if (x > 0 && y != 0) {
            x += y * 2;
        }
        return 0;
    }
    '''

    lexer = Lexer(sample)
    tokens = lexer.tokenize()
    for t in tokens:
        print(t)
