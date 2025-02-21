#parser.py

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
        if self.peek().type == TokenType.LEFT_BRACE:
            return self.parse_block()
        if self.peek().type == TokenType.PRINT:
            self.consume(TokenType.PRINT)
            expr = self.assignment_expr()
            return Print(expr)
        elif self.peek().type == TokenType.WHILE:
            self.consume(TokenType.WHILE)
            condition = self.assignment_expr()
            # Check if a block is provided for the loop body
            if self.peek().type == TokenType.LEFT_BRACE:
                body = self.parse_block()
            else:
                body = self.parse_statement()
            return While(condition, body)
        elif self.peek().type == TokenType.IF:
            self.consume(TokenType.IF)
            # Parse the condition for the if statement
            condition = self.assignment_expr()
            # Expect the THEN keyword
            self.consume(TokenType.THEN)
            # Parse the then branch (could be a single statement or block)
            then_branch = self.parse_statement()
            
            # Check for an optional ELSE branch
            else_branch = None
            if self.peek().type == TokenType.ELSE:
                self.consume(TokenType.ELSE)
                else_branch = self.parse_statement()
            
            return If(condition, then_branch, else_branch)
        else:
            return self.assignment_expr()

    def parse_block(self):
        statements = []
        self.consume(TokenType.LEFT_BRACE)  # Expect opening {
        while self.peek().type != TokenType.RIGHT_BRACE:
            statements.append(self.parse_statement())
        self.consume(TokenType.RIGHT_BRACE)  # Expect closing }
        return Block(statements)
    
    def parse_program(self):
        statements = []
        while self.peek().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return Block(statements)

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
    
    # parse_list_literal -> '[' (assignment_expr (',' assignment_expr)*)? ']'
    def parse_list_literal(self):
        elements = []
        self.consume(TokenType.LEFT_BRACKET)  # Consume '['
        # Handle empty list case
        if self.peek().type == TokenType.RIGHT_BRACKET:
            self.consume(TokenType.RIGHT_BRACKET)
            return ListLiteral(elements)
        
        # Parse list elements separated by commas.
        while True:
            elem = self.assignment_expr()
            elements.append(elem)
            if self.peek().type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
            else:
                break
        self.consume(TokenType.RIGHT_BRACKET)  # Consume ']'
        return ListLiteral(elements)

    def factor(self):
        # Prefix operators
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
            node = self.parse_list_literal()  # (Already implemented for list literals)
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
        
        # Handle member calls: e.g., myList.push_back(5)
        while self.peek().type == TokenType.DOT:
            self.consume(TokenType.DOT)  # Consume the dot.
            member_token = self.consume(TokenType.IDENTIFIER)  # The member name.
            member_name = member_token.value
            # Check if it's a call by looking for '('
            if self.peek().type == TokenType.LEFT_PAREN:
                self.consume(TokenType.LEFT_PAREN)
                arguments = []
                if self.peek().type != TokenType.RIGHT_PAREN:
                    while True:
                        arguments.append(self.assignment_expr())
                        if self.peek().type == TokenType.COMMA:
                            self.consume(TokenType.COMMA)
                        else:
                            break
                self.consume(TokenType.RIGHT_PAREN)
                node = MemberCall(node, member_name, arguments)
            else:
                # Optionally support property access.
                raise SyntaxError("Expected '(' after member name for method call")
        
        # Handle list access (postfix operator)
        while self.peek().type == TokenType.LEFT_BRACKET:
            self.consume(TokenType.LEFT_BRACKET)
            index_expr = self.assignment_expr()  # or another expression method if desired
            self.consume(TokenType.RIGHT_BRACKET)
            node = ListAccess(node, index_expr)
        
        return node
