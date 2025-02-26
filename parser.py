# parser.py
# The parser.py file contains the Parser class, which is responsible for parsing the tokens produced by the Tokenizer into an Abstract Syntax Tree (AST). 
# The AST represents the structure of the program in a hierarchical form that can be easily evaluated by the Interpreter.

from lexer import TokenType  # TokenType now includes TRUE, FALSE, NOT, AND, OR, EQUALS, etc.
from ast_nodes import *  # Import all classes from ast_nodes.py

class Parser:
    """Parses a list of tokens into an Abstract Syntax Tree (AST)."""
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
        token_type = self.peek().type
        if token_type == TokenType.RETURN:
            self.consume(TokenType.RETURN)
            value = self.assignment_expr()
            return Return(value)
        elif token_type == TokenType.FUN:
            return self.parse_function_declaration()
        elif token_type == TokenType.LEFT_BRACE:
            return self.parse_block()
        elif token_type == TokenType.PRINT:
            self.consume(TokenType.PRINT)
            expr = self.assignment_expr()
            return Print(expr)
        elif token_type == TokenType.WHILE:
            self.consume(TokenType.WHILE)
            condition = self.assignment_expr()
            body = self.parse_block() if self.peek().type == TokenType.LEFT_BRACE else self.parse_statement()
            return While(condition, body)
        elif token_type == TokenType.IF:
            self.consume(TokenType.IF)
            condition = self.assignment_expr()
            self.consume(TokenType.THEN)
            then_branch = self.parse_statement()
            else_branch = None
            if self.peek().type == TokenType.ELSE:
                self.consume(TokenType.ELSE)
                else_branch = self.parse_statement()
            return If(condition, then_branch, else_branch)
        else:
            return self.assignment_expr()

    def parse_function_declaration(self):
        self.consume(TokenType.FUN)  # Consume 'fun'
        name_token = self.consume(TokenType.IDENTIFIER)
        name = name_token.value
        self.consume(TokenType.LEFT_PAREN)  # Consume '('
        parameters = []
        if self.peek().type != TokenType.RIGHT_PAREN:
            parameters.append(self.consume(TokenType.IDENTIFIER).value)
            while self.peek().type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
                parameters.append(self.consume(TokenType.IDENTIFIER).value)
        self.consume(TokenType.RIGHT_PAREN)  # Consume ')'
        body = self.parse_block()            # Parse the function body as a block
        return Function(name, parameters, body)

    def parse_block(self):
        statements = []
        self.consume(TokenType.LEFT_BRACE)  # Expect opening '{'
        while self.peek().type != TokenType.RIGHT_BRACE:
            statements.append(self.parse_statement())
        self.consume(TokenType.RIGHT_BRACE)  # Expect closing '}'
        return Block(statements)

    def parse_program(self):
        statements = []
        while self.peek().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return Block(statements)

    def parse(self):
        return self.parse_statement()

    def assignment_expr(self):
        node = self.equality_expr()
        while self.peek().type == TokenType.ASSIGN:
            self.consume(TokenType.ASSIGN)
            value = self.assignment_expr()  # Right-hand side
            node = Assignment(node, value)
        return node

    def or_expr(self):
        node = self.and_expr()
        while self.peek().type == TokenType.OR:
            op = self.consume(TokenType.OR)
            right = self.and_expr()
            node = Binary(node, op.value, right)
        return node

    def and_expr(self):
        node = self.equality_expr()
        while self.peek().type == TokenType.AND:
            op = self.consume(TokenType.AND)
            right = self.equality_expr()
            node = Binary(node, op.value, right)
        return node

    def equality_expr(self):
        node = self.relational_expr()
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

    def add_expr(self):
        node = self.mult_expr()
        while self.peek().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.consume(self.peek().type)
            right = self.mult_expr()
            node = Binary(node, op.value, right)
        return node

    def mult_expr(self):
        node = self.factor()
        while self.peek().type in (TokenType.STAR, TokenType.SLASH):
            op = self.consume(self.peek().type)
            right = self.factor()
            node = Binary(node, op.value, right)
        return node

    def parse_list_literal(self):
        elements = []
        self.consume(TokenType.LEFT_BRACKET)  # Consume '['
        if self.peek().type == TokenType.RIGHT_BRACKET:
            self.consume(TokenType.RIGHT_BRACKET)
            return ListLiteral(elements)
        while True:
            elem = self.assignment_expr()
            elements.append(elem)
            if self.peek().type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
            else:
                break
        self.consume(TokenType.RIGHT_BRACKET)  # Consume ']'
        return ListLiteral(elements)

    def parse_arguments(self):
        """Helper to parse comma-separated arguments within parentheses."""
        args = []
        self.consume(TokenType.LEFT_PAREN)  # Consume '('
        if self.peek().type != TokenType.RIGHT_PAREN:
            args.append(self.assignment_expr())
            while self.peek().type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
                args.append(self.assignment_expr())
        self.consume(TokenType.RIGHT_PAREN)  # Consume ')'
        return args

    def parse_postfix(self, node):
        """Helper to handle postfix operators: function calls, member access, and list indexing."""
        while self.peek().type in (TokenType.LEFT_PAREN, TokenType.DOT, TokenType.LEFT_BRACKET):
            if self.peek().type == TokenType.LEFT_PAREN:
                args = self.parse_arguments()
                node = Call(node, args)
            elif self.peek().type == TokenType.DOT:
                self.consume(TokenType.DOT)  # Consume '.'
                member_token = self.consume(TokenType.IDENTIFIER)
                member_name = member_token.value
                if self.peek().type == TokenType.LEFT_PAREN:
                    args = self.parse_arguments()
                    node = MemberCall(node, member_name, args)
                else:
                    raise SyntaxError("Expected '(' after member name for method call")
            elif self.peek().type == TokenType.LEFT_BRACKET:
                self.consume(TokenType.LEFT_BRACKET)
                index_expr = self.assignment_expr()
                self.consume(TokenType.RIGHT_BRACKET)
                node = ListAccess(node, index_expr)
        return node

    def factor(self):
        token = self.peek()
        if token.type == TokenType.NUMBER:
            self.consume(TokenType.NUMBER)
            node = Number(token.value)
        elif token.type == TokenType.STRING:
            self.consume(TokenType.STRING)
            node = StringLiteral(token.value)
        elif token.type == TokenType.TRUE:
            self.consume(TokenType.TRUE)
            node = BooleanLiteral(True)
        elif token.type == TokenType.FALSE:
            self.consume(TokenType.FALSE)
            node = BooleanLiteral(False)
        elif token.type == TokenType.IDENTIFIER:
            self.consume(TokenType.IDENTIFIER)
            node = Identifier(token.value)
        elif token.type == TokenType.LEFT_PAREN:
            self.consume(TokenType.LEFT_PAREN)
            node = self.or_expr()
            self.consume(TokenType.RIGHT_PAREN)
        elif token.type == TokenType.LEFT_BRACKET:
            node = self.parse_list_literal()
        elif token.type == TokenType.MINUS:
            op = self.consume(TokenType.MINUS)
            right = self.factor()
            node = Unary(op.value, right)
        elif token.type == TokenType.NOT:
            op = self.consume(TokenType.NOT)
            right = self.factor()
            node = Unary(op.value, right)
        else:
            raise SyntaxError(f"Unexpected token: {token}")
        return self.parse_postfix(node)
