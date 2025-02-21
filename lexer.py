# lexer.py: Contains the Token and Tokenizer classes, which are used to tokenize the input string.

from enum import Enum

class TokenType(Enum):
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
    PRINT          = "PRINT"       # <-- New token type for print
    WHILE          = "WHILE"      # New token for while loops
    LEFT_BRACE     = "LEFT_BRACE"   # for {
    RIGHT_BRACE    = "RIGHT_BRACE"  # for }
    IF             = "IF"         # New token for if statements
    THEN           = "THEN"       # New token for then keyword
    ELSE           = "ELSE"    # <-- New token type for else
    LEFT_BRACKET   = "LEFT_BRACKET"   # for [
    RIGHT_BRACKET  = "RIGHT_BRACKET"  # for ]
    COMMA          = "COMMA"          # for ,
    DOT            = "DOT"  # For '.'
    FUN            = "FUN"       # New: function declaration
    RETURN         = "RETURN"    # New: return keyword

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Tokenizer:
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

    def tokenize(self):
        while self.current < len(self.source):
            ch = self.advance()
            # Skip whitespace
            if ch.isspace():
                continue

            # Skip comments (everything until the end of the line)
            if ch == '#':
                while self.peek() is not None and self.peek() != '\n':
                    self.advance()
                continue

            # Numbers (including decimals)
            # Only treat a dot as part of a number if it is followed by a digit.
            if ch.isdigit() or (ch == '.' and self.peek() is not None and self.peek().isdigit()):
                num_value = ch
                while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
                    num_value += self.advance()
                self.tokens.append(Token(TokenType.NUMBER, float(num_value)))
                continue

            # If a dot is not part of a number, treat it as DOT.
            if ch == '.':
                self.tokens.append(Token(TokenType.DOT, ch))
                continue

            if ch == '{':
                self.tokens.append(Token(TokenType.LEFT_BRACE, ch))
                continue

            if ch == '}':
                self.tokens.append(Token(TokenType.RIGHT_BRACE, ch))
                continue

            if ch.isalpha():
                ident = ch
                while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
                    ident += self.advance()
                # Reserved keywords (true, false, and, or, not, etc.)
                lower_ident = ident.lower()
                if lower_ident == "true":
                    self.tokens.append(Token(TokenType.TRUE, ident))
                elif lower_ident == "false":
                    self.tokens.append(Token(TokenType.FALSE, ident))
                elif lower_ident == "and":
                    self.tokens.append(Token(TokenType.AND, ident))
                elif lower_ident == "or":
                    self.tokens.append(Token(TokenType.OR, ident))
                elif lower_ident == "not":
                    self.tokens.append(Token(TokenType.NOT, ident))
                elif lower_ident == "print":
                    self.tokens.append(Token(TokenType.PRINT, ident))
                elif lower_ident == "while":
                    self.tokens.append(Token(TokenType.WHILE, ident))
                elif lower_ident == "if":
                    self.tokens.append(Token(TokenType.IF, ident))
                elif lower_ident == "then":
                    self.tokens.append(Token(TokenType.THEN, ident))
                elif lower_ident == "else":
                    self.tokens.append(Token(TokenType.ELSE, ident))
                elif lower_ident == "fun": 
                    self.tokens.append(Token(TokenType.FUN, ident))
                elif lower_ident == "return":
                    self.tokens.append(Token(TokenType.RETURN, ident))
                else:
                    self.tokens.append(Token(TokenType.IDENTIFIER, ident))
                continue

            # Single-character tokens for lists
            if ch == '[':
                self.tokens.append(Token(TokenType.LEFT_BRACKET, ch))
                continue

            if ch == ']':
                self.tokens.append(Token(TokenType.RIGHT_BRACKET, ch))
                continue

            if ch == ',':
                self.tokens.append(Token(TokenType.COMMA, ch))
                continue

            # Single-character arithmetic tokens
            if ch == '+':
                self.tokens.append(Token(TokenType.PLUS, ch))
                continue
            if ch == '-':
                self.tokens.append(Token(TokenType.MINUS, ch))
                continue
            if ch == '*':
                self.tokens.append(Token(TokenType.STAR, ch))
                continue
            if ch == '/':
                self.tokens.append(Token(TokenType.SLASH, ch))
                continue
            if ch == '(':
                self.tokens.append(Token(TokenType.LEFT_PAREN, ch))
                continue
            if ch == ')':
                self.tokens.append(Token(TokenType.RIGHT_PAREN, ch))
                continue

            if ch == '=':
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.EQUALS, "=="))  # Equality check
                else:
                    self.tokens.append(Token(TokenType.ASSIGN, "="))  # Assignment
                continue

            if ch == '!':
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.NOT_EQUALS, "!="))
                else:
                    # Allow "!" as a shorthand for NOT.
                    self.tokens.append(Token(TokenType.NOT, ch))
                continue
            if ch == '<':
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.LESS_EQ, "<="))
                else:
                    self.tokens.append(Token(TokenType.LESS, ch))
                continue
            if ch == '>':
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.GREATER_EQ, ">="))
                else:
                    self.tokens.append(Token(TokenType.GREATER, ch))
                continue

            if ch == '"':
                string_value = ""
                # Loop until the closing quote is found
                while True:
                    ch = self.advance()
                    if ch is None:
                        raise SyntaxError("Unterminated string literal")
                    if ch == '"':
                        break
                    # Optionally handle escape sequences here
                    string_value += ch
                self.tokens.append(Token(TokenType.STRING, string_value))
                continue

            raise SyntaxError(f"Unexpected character: '{ch}'")

        self.tokens.append(Token(TokenType.EOF, None))
        return self.tokens


