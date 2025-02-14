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
    
class Block(Expr):
    def __init__(self, statements):
        self.statements = statements  # List of statements/expressions
    def __repr__(self):
        return f"Block({self.statements})"
    
class If(Expr):
    def __init__(self, condition, then_branch):
        self.condition = condition
        self.then_branch = then_branch
    def __repr__(self):
        return f"If({self.condition}, {self.then_branch})"
    
class If(Expr):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch  # Optional else branch
    def __repr__(self):
        if self.else_branch:
            return f"If({self.condition}, {self.then_branch}, {self.else_branch})"
        else:
            return f"If({self.condition}, {self.then_branch})"
        
class ListLiteral(Expr):
    def __init__(self, elements):
        self.elements = elements  # A list of expressions

    def __repr__(self):
        return f"ListLiteral({self.elements})"
    
class ListAccess(Expr):
    def __init__(self, list_expr, index_expr):
        self.list_expr = list_expr
        self.index_expr = index_expr
    def __repr__(self):
        return f"ListAccess({self.list_expr}, {self.index_expr})"
