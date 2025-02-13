from lexer import TokenType  # TokenType now includes TRUE, FALSE, NOT, AND, OR, EQUALS, etc.
from ast_nodes import * # Import all classes from ast_nodes.py

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek(self):
        return self.tokens[self.current]

    def consume(self, expected_type):
        token = self.peek()
        if token.type == expected_type:
            self.current += 1
            return token
        raise SyntaxError(f"Expected token type {expected_type}, but got {token.type}")

    def parse_statement(self):
        if self.peek().type == TokenType.PRINT:
            self.consume(TokenType.PRINT)
            expr = self.assignment_expr()
            return Print(expr)
        elif self.peek().type == TokenType.WHILE:
            self.consume(TokenType.WHILE)
            # Parse the condition expression.
            condition = self.assignment_expr()
            # Parse the loop body.
            # For simplicity, we assume the body is a single statement.
            body = self.parse_statement()
            return While(condition, body)
        else:
            return self.assignment_expr()

    def parse(self):
        # Use the statement parser instead of just assignment_expr
        return self.parse_statement()

    def assignment_expr(self):
        node = self.equality_expr()  # Ensure full expressions are parsed

        while self.peek().type == TokenType.ASSIGN:  # If there's an assignment operator (`=`)
            self.consume(TokenType.ASSIGN)
            value = self.assignment_expr()  # Recursively parse the right-hand side
            node = Assignment(node, value)

        return node

    def binary_expr(self, left=None):
        if left is None:
            left = self.add_expr()  # Start from addition expressions

        while self.peek().type in (TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH):
            op = self.consume(self.peek().type)
            right = self.add_expr()  # Parse the right-hand side
            left = Binary(left, op.value, right)  # Create a Binary node

        return left
    # or_expr -> and_expr ( OR and_expr )*
    def or_expr(self):
        node = self.and_expr()
        while self.peek().type == TokenType.OR:
            op = self.consume(TokenType.OR)
            right = self.and_expr()
            node = Binary(node, op.value, right)
        return node

    # and_expr -> equality_expr ( AND equality_expr )*
    def and_expr(self):
        node = self.equality_expr()
        while self.peek().type == TokenType.AND:
            op = self.consume(TokenType.AND)
            right = self.equality_expr()
            node = Binary(node, op.value, right)
        return node

    def equality_expr(self):
        node = self.relational_expr()  # Use relational_expr here
        while self.peek().type in (TokenType.EQUALS, TokenType.NOT_EQUALS):
            op = self.consume(self.peek().type)
            right = self.relational_expr()
            node = Binary(node, op.value, right)
        return node

    def relational_expr(self):
        node = self.add_expr()
        while self.peek().type in (TokenType.LESS, TokenType.GREATER,
                                    TokenType.LESS_EQ, TokenType.GREATER_EQ):
            op = self.consume(self.peek().type)
            right = self.add_expr()
            node = Binary(node, op.value, right)
        return node

    # add_expr -> mult_expr ( (PLUS | MINUS) mult_expr )*
    def add_expr(self):
        node = self.mult_expr()
        while self.peek().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.consume(self.peek().type)
            right = self.mult_expr()
            node = Binary(node, op.value, right)
        return node

    # mult_expr -> factor ( (STAR | SLASH) factor )*
    def mult_expr(self):
        node = self.factor()
        while self.peek().type in (TokenType.STAR, TokenType.SLASH):
            op = self.consume(self.peek().type)
            right = self.factor()
            node = Binary(node, op.value, right)
        return node

    def factor(self):
        token = self.peek()

        if token.type == TokenType.NUMBER:
            self.consume(TokenType.NUMBER)
            return Number(token.value)
        
        if token.type == TokenType.STRING:
            self.consume(TokenType.STRING)
            return StringLiteral(token.value)

        if token.type == TokenType.TRUE:
            self.consume(TokenType.TRUE)
            return BooleanLiteral(True)

        if token.type == TokenType.FALSE:
            self.consume(TokenType.FALSE)
            return BooleanLiteral(False)

        if token.type == TokenType.IDENTIFIER:
            self.consume(TokenType.IDENTIFIER)
            return Identifier(token.value)

        if token.type == TokenType.LEFT_PAREN:
            self.consume(TokenType.LEFT_PAREN)
            node = self.or_expr()  # Evaluate the expression inside parentheses
            self.consume(TokenType.RIGHT_PAREN)
            return node

        if token.type == TokenType.MINUS:
            op = self.consume(TokenType.MINUS)
            right = self.factor()
            return Unary(op.value, right)

        if token.type == TokenType.NOT:
            op = self.consume(TokenType.NOT)
            right = self.factor()
            return Unary(op.value, right)

        raise SyntaxError(f"Unexpected token: {token}")
