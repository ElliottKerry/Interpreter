import os
import sys
import platform
from lexer import Tokenizer
from parser import Parser
from interpreter import Interpreter


def read_file(file_path):
    """Reads the entire file content as a single string."""
    with open(file_path, 'r') as file:
        return file.read()

def main(file_path):
    # Read the entire program as one string.
    program_source = read_file(file_path)
    
    # Create an interpreter instance.
    interpreter = Interpreter()
    
    try:
        # Tokenize the entire program.
        tokenizer = Tokenizer(program_source)
        tokens = tokenizer.tokenize()
        print(f"\nTokens: {tokens}\n")
        
        # Parse the tokens into an AST for the whole program.
        parser = Parser(tokens)
        ast = parser.parse_program()
        print(f"AST: {ast}\n")
        
        # Evaluate the AST.
        interpreter.evaluate(ast)
        
    except Exception as e:
        print(f"Error: {e}")

def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

if __name__ == "__main__":
    # Use command-line arguments if provided; otherwise, default to 'expressions.txt'
    clear_terminal()
    file_path = sys.argv[1] if len(sys.argv) > 1 else 'expressions.txt'
    main(file_path)
