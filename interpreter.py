# interpreter.py
# The Interpreter class is responsible for evaluating the AST nodes produced by the parser. It contains a series of evaluate methods for each AST node type.
# The evaluate method for each node type is responsible for evaluating the node and returning the result. 
# The Interpreter class also contains a call_function method that is used to call user-defined functions.

from parser import *  # Adjust your import based on your project structure

class Interpreter:
    """Evaluates an Abstract Syntax Tree (AST) produced by the Parser."""
    def __init__(self):
        self.variables = {}  # Store global variables

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

        elif isinstance(expr, Assignment):
            value = self.evaluate(expr.value)
            # Check if the assignment target is an Identifier.
            if isinstance(expr.target, Identifier):
                self.variables[expr.target.name] = value
                return value
            # Else if the target is a ListAccess, update the element at that index.
            elif isinstance(expr.target, ListAccess):
                list_val = self.evaluate(expr.target.list_expr)
                index_val = self.evaluate(expr.target.index_expr)
                try:
                    list_val[int(index_val)] = value
                except Exception as e:
                    raise Exception(f"Error assigning list element at index {index_val}: {e}")
                return value
            else:
                raise Exception("Invalid assignment target")

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

        elif isinstance(expr, Function):
            # A function definition evaluates to itself and is stored in the global environment.
            self.variables[expr.name] = expr
            return expr

        elif isinstance(expr, Return):
            return self.evaluate(expr.value)

        elif isinstance(expr, Call):
            callee = self.evaluate(expr.callee)
            args = [self.evaluate(arg) for arg in expr.arguments]
            if isinstance(callee, Function):
                return self.call_function(callee, args)
            else:
                raise Exception("Attempted to call a non-function")

        elif isinstance(expr, MemberCall):
            object_val = self.evaluate(expr.object_expr)
            args = [self.evaluate(arg) for arg in expr.arguments]
            if isinstance(object_val, list):
                if expr.member_name == "push_back":
                    if len(args) != 1:
                        raise Exception("push_back requires exactly one argument")
                    object_val.append(args[0])
                    return object_val
                elif expr.member_name == "remove":
                    if len(args) != 1:
                        raise Exception("remove requires exactly one argument (the index to remove)")
                    try:
                        index = int(args[0])
                        removed = object_val.pop(index)
                        return removed
                    except Exception as e:
                        raise Exception(f"Error removing element at index {args[0]}: {e}")
                else:
                    raise Exception(f"Unknown member function '{expr.member_name}' on list")
            else:
                raise Exception(f"Member call on unsupported object type: {object_val}")

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
                # If a Return node is encountered, propagate it immediately.
                if isinstance(result, Return):
                    return result
            return result
                            
        elif isinstance(expr, While):
            while self.evaluate(expr.condition):
                result = self.evaluate(expr.body)
                if isinstance(result, Return):
                    return result
            return None
            
        elif isinstance(expr, Print):
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

    def call_function(self, func, args):
        # Check parameter count
        if len(args) != len(func.parameters):
            raise Exception("Function argument count mismatch")
        # Create a new environment for function execution.
        # For simplicity, copy the current global environment.
        local_env = self.variables.copy()
        for param, arg in zip(func.parameters, args):
            local_env[param] = arg
        # Save the old environment.
        old_env = self.variables
        self.variables = local_env
        try:
            result = self.evaluate(func.body)
            # If a return statement was encountered, extract its value.
            if isinstance(result, Return):
                result = result.value
            return result
        finally:
            self.variables = old_env
