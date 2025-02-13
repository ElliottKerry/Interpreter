import sys
from lexer import Tokenizer
from parser import Parser
from interpreter import Interpreter

def read_file(file_path):
    """Reads a file and returns a list of expressions."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def process_expression(expr, interpreter):
    """
    Process a single expression: tokenize, parse, and evaluate.
    
    Returns the result of evaluating the expression.
    """

    # Tokenize the expression.
    tokenizer = Tokenizer(expr)
    tokens = tokenizer.tokenize()
    print(f"Tokens: {tokens}")

    # Parse the tokens into an AST.
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"AST: {ast}")

    # Evaluate the AST.
    return interpreter.evaluate(ast)

def main(file_path):
    expressions = read_file(file_path)
    
    # Create an interpreter instance once if it maintains no state across expressions.
    interpreter = Interpreter()
    
    for expr in expressions:
        try:
            if expr.startswith("#"): # Skip comments
                continue

            result = process_expression(expr, interpreter)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"Error processing '{expr}': {e}")

if __name__ == "__main__":
    # Use command-line arguments if provided; otherwise, default to 'expressions.txt'
    file_path = sys.argv[1] if len(sys.argv) > 1 else 'expressions.txt'
    main(file_path)
