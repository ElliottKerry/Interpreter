# interpreter.py
from parser import *  # Adjust your import based on your project structure

class Interpreter:
    def __init__(self):
        self.variables = {}  # Store variable values

    def evaluate(self, expr):
        if isinstance(expr, Number):
            return expr.value

        elif isinstance(expr, StringLiteral):
            return expr.value

        elif isinstance(expr, BooleanLiteral):
            return expr.value

        elif isinstance(expr, Identifier):  # Lookup variable
            if expr.name in self.variables:
                return self.variables[expr.name]
            raise Exception(f"Undefined variable: {expr.name}")

        elif isinstance(expr, Assignment):  # Handle assignments
            value = self.evaluate(expr.value)  # Ensure the right-hand side is evaluated
            self.variables[expr.identifier.name] = value  # Store the new value
            return value  # Return updated value

        elif isinstance(expr, Binary):
            left_val = self.evaluate(expr.left)
            right_val = self.evaluate(expr.right)

            if expr.operator == "+":
                # If one operand is a string, convert both to strings for concatenation.
                if isinstance(left_val, str) or isinstance(right_val, str):
                    return str(left_val) + str(right_val)
                return left_val + right_val

            elif expr.operator == "-":
                return left_val - right_val
            elif expr.operator == "*":
                return left_val * right_val
            elif expr.operator == "/":
                return round(left_val / right_val, 2)  # With rounding support
            elif expr.operator == "==":
                return left_val == right_val
            elif expr.operator == "!=":
                return left_val != right_val
            elif expr.operator == "<":
                return left_val < right_val
            elif expr.operator == ">":
                return left_val > right_val
            elif expr.operator == "<=":
                return left_val <= right_val
            elif expr.operator == ">=":
                return left_val >= right_val
            elif expr.operator == "and":
                return left_val and right_val
            elif expr.operator == "or":
                return left_val or right_val

        elif isinstance(expr, Unary):
            operand = self.evaluate(expr.operand)
            if expr.operator in ("!", "not"):
                return not operand
            elif expr.operator == "-":
                return -operand
            else:
                raise Exception(f"Unknown unary operator: {expr.operator}")
            
        elif isinstance(expr, Block):
            result = None
            for statement in expr.statements:
                result = self.evaluate(statement)
            return result
                    
        elif isinstance(expr, While):
            # Evaluate the condition and execute the body as long as it's true.
            while self.evaluate(expr.condition):
                self.evaluate(expr.body)
            # Optionally return None (or some appropriate value) after the loop finishes.
            return None
            
        elif isinstance(expr, Print):
            # Evaluate the expression and print its result
            value = self.evaluate(expr.expr)
            print(">>", value)
            return value
        
        elif isinstance(expr, ListAccess):
            list_val = self.evaluate(expr.list_expr)
            index_val = self.evaluate(expr.index_expr)
            try:
                return list_val[int(index_val)]
            except Exception as e:
                raise Exception(f"Error accessing list at index {index_val}: {e}")
                
        elif isinstance(expr, ListLiteral):
            # Evaluate each element in the list and return a Python list.
            return [self.evaluate(element) for element in expr.elements]
            
        elif isinstance(expr, If):
            if self.evaluate(expr.condition):
                return self.evaluate(expr.then_branch)
            elif expr.else_branch is not None:
                return self.evaluate(expr.else_branch)
            else:
                return None
                        
        else:
            raise Exception("Unknown expression type")
