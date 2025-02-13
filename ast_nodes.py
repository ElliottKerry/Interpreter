# ast_nodes.py

class Expr:
    pass

class Number(Expr):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Number({self.value})"

class BooleanLiteral(Expr):
    def __init__(self, value: bool):
        self.value = value
    def __repr__(self):
        return f"BooleanLiteral({self.value})"

class Unary(Expr):
    def __init__(self, operator, operand):
        self.operator = operator  # e.g., "!" or "not"
        self.operand = operand
    def __repr__(self):
        return f"UnaryOp({self.operator}, {self.operand})"

class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator  # e.g., "+", "-", "==", "and", "or", "<", etc.
        self.right = right
    def __repr__(self):
        return f"Binary({self.left}, {self.operator}, {self.right})"
    
class StringLiteral(Expr):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'StringLiteral({repr(self.value)})'

class Identifier(Expr):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Identifier({self.name})"

class Assignment(Expr):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value
    def __repr__(self):
        return f"Assignment({self.identifier}, {self.value})"
    
class Print(Expr):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return f"Print({self.expr})"
    
class While(Expr):
    def __init__(self, condition, body):
        self.condition = condition  # An expression that evaluates to True/False.
        self.body = body            # The body is typically a statement or a block.
    def __repr__(self):
        return f"While({self.condition}, {self.body})"