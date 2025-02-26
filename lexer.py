# lexer.py: Contains the Token and Tokenizer classes, which are used to tokenize the input string, 

from enum import Enum

class TokenType(Enum):
    """Enumeration of token types"""
    NUMBER         = "NUMBER"
    STRING         = "STRING"
    PLUS           = "PLUS"
    MINUS          = "MINUS"
    STAR           = "STAR"
    SLASH          = "SLASH"
    LEFT_PAREN     = "LEFT_PAREN"
    RIGHT_PAREN    = "RIGHT_PAREN"
    TRUE           = "TRUE"
    FALSE          = "FALSE"
    EQUALS         = "EQUALS"      # for ==
    NOT_EQUALS     = "NOT_EQUALS"  # for !=
    LESS           = "LESS"        # for <
    GREATER        = "GREATER"     # for >
    LESS_EQ        = "LESS_EQ"     # for <=
    GREATER_EQ     = "GREATER_EQ"  # for >=
    NOT            = "NOT"         # for ! (or you could also support "not")
    AND            = "AND"         # for and
    OR             = "OR"          # for or
    EOF            = "EOF"
    IDENTIFIER     = "IDENTIFIER"  # Variables
    ASSIGN         = "ASSIGN"      # Single '='
    PRINT          = "PRINT"       # for print
    WHILE          = "WHILE"       # for while loops
    LEFT_BRACE     = "LEFT_BRACE"  # for {
    RIGHT_BRACE    = "RIGHT_BRACE" # for }
    IF             = "IF"          # for if statements
    THEN           = "THEN"        # for then keyword
    ELSE           = "ELSE"        # for else
    LEFT_BRACKET   = "LEFT_BRACKET"  # for [
    RIGHT_BRACKET  = "RIGHT_BRACKET" # for ]
    COMMA          = "COMMA"         # for ,
    DOT            = "DOT"           # for '.'
    FUN            = "FUN"           # for function declaration
    RETURN         = "RETURN"        # for return keyword

class Token:
    """Represents a token with a type and an optional value."""
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Tokenizer:
    """Tokenizes the input source code."""
    # Single-character tokens mapping.
    SINGLE_CHAR_TOKENS = {
        '.': TokenType.DOT,
        '{': TokenType.LEFT_BRACE,
        '}': TokenType.RIGHT_BRACE,
        '[': TokenType.LEFT_BRACKET,
        ']': TokenType.RIGHT_BRACKET,
        ',': TokenType.COMMA,
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.STAR,
        '/': TokenType.SLASH,
        '(': TokenType.LEFT_PAREN,
        ')': TokenType.RIGHT_PAREN,
    }

    # Reserved keywords mapping.
    KEYWORDS = {
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
        "and": TokenType.AND,
        "or": TokenType.OR,
        "not": TokenType.NOT,
        "print": TokenType.PRINT,
        "while": TokenType.WHILE,
        "if": TokenType.IF,
        "then": TokenType.THEN,
        "else": TokenType.ELSE,
        "fun": TokenType.FUN,
        "return": TokenType.RETURN,
    }

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.current = 0

    def advance(self):
        if self.current < len(self.source):
            ch = self.source[self.current]
            self.current += 1
            return ch
        return None

    def peek(self):
        if self.current < len(self.source):
            return self.source[self.current]
        return None

    def match(self, expected):
        if self.peek() == expected:
            self.advance()
            return True
        return False

    def add_token(self, token_type, value):
        self.tokens.append(Token(token_type, value))

    def tokenize(self):
        while self.current < len(self.source):
            ch = self.advance()

            # Skip whitespace.
            if ch.isspace():
                continue

            # Skip comments.
            if ch == '#':
                while self.peek() is not None and self.peek() != '\n':
                    self.advance()
                continue

            # Numbers (handle decimals).
            if ch.isdigit() or (ch == '.' and self.peek() and self.peek().isdigit()):
                self.tokenize_number(ch)
                continue

            # String literals.
            if ch == '"':
                self.tokenize_string()
                continue

            # Identifiers and keywords.
            if ch.isalpha():
                self.tokenize_identifier(ch)
                continue

            # Single-character tokens.
            if ch in self.SINGLE_CHAR_TOKENS:
                self.add_token(self.SINGLE_CHAR_TOKENS[ch], ch)
                continue

            # Multi-character tokens.
            if ch == '=':
                if self.match('='):
                    self.add_token(TokenType.EQUALS, "==")
                else:
                    self.add_token(TokenType.ASSIGN, "=")
                continue

            if ch == '!':
                if self.match('='):
                    self.add_token(TokenType.NOT_EQUALS, "!=")
                else:
                    self.add_token(TokenType.NOT, "!")
                continue

            if ch == '<':
                if self.match('='):
                    self.add_token(TokenType.LESS_EQ, "<=")
                else:
                    self.add_token(TokenType.LESS, "<")
                continue

            if ch == '>':
                if self.match('='):
                    self.add_token(TokenType.GREATER_EQ, ">=")
                else:
                    self.add_token(TokenType.GREATER, ">")
                continue

            raise SyntaxError(f"Unexpected character: '{ch}'")

        self.add_token(TokenType.EOF, None)
        return self.tokens

    def tokenize_number(self, first_char):
        num_str = first_char
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            num_str += self.advance()
        # Determine if the number is an int or a float.
        if '.' in num_str:
            value = float(num_str)
        else:
            value = int(num_str)
        self.add_token(TokenType.NUMBER, value)

    def tokenize_identifier(self, first_char):
        ident = first_char
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            ident += self.advance()
        # Check if the identifier is a reserved keyword.
        token_type = self.KEYWORDS.get(ident.lower(), TokenType.IDENTIFIER)
        self.add_token(token_type, ident)

    def tokenize_string(self):
        string_value = ""
        while True:
            ch = self.advance()
            if ch is None:
                raise SyntaxError("Unterminated string literal")
            if ch == '"':
                break
            string_value += ch
        self.add_token(TokenType.STRING, string_value)
