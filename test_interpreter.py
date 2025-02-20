# test_interpreter.py
# This file contains comprehensive tests for the interpreter.
# We’re testing everything—from basic arithmetic to control flow and advanced features.
# Unit tests are critical to ensure our interpreter works perfectly, and these tests are fantastic.

import pytest
from lexer import Tokenizer
from parser import Parser
from interpreter import Interpreter

# A pytest fixture to create a fresh interpreter for each test.
@pytest.fixture
def interpreter():
    return Interpreter()

# A helper function to run a source string through the interpreter.
def run_program(source, interpreter):
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_program()
    return interpreter.evaluate(ast)

# ---------------------------
# Stage 1: Basic Calculator Tests
# ---------------------------

def test_arithmetic_addition(interpreter):
    source = '{ i = 5 + 3 }'
    run_program(source, interpreter)
    assert interpreter.variables.get("i") == 8

def test_arithmetic_subtraction(interpreter):
    source = '{ i = 10 - 2 }'
    run_program(source, interpreter)
    assert interpreter.variables.get("i") == 8

def test_arithmetic_multiplication(interpreter):
    source = '{ i = 3 * 4 }'
    run_program(source, interpreter)
    assert interpreter.variables.get("i") == 12

def test_arithmetic_division(interpreter):
    source = '{ i = 12 / 4 }'
    run_program(source, interpreter)
    assert interpreter.variables.get("i") == 3

def test_arithmetic_parentheses(interpreter):
    source = '{ i = (2 + 3) * 4 }'
    run_program(source, interpreter)
    assert interpreter.variables.get("i") == 20

def test_arithmetic_unary_negation(interpreter):
    source = '{ i = -5 }'
    run_program(source, interpreter)
    assert interpreter.variables.get("i") == -5

# ---------------------------
# Stage 2: Boolean Logic Tests
# ---------------------------

def test_boolean_equality(interpreter):
    source = '{ result = true == true }'
    run_program(source, interpreter)
    assert interpreter.variables.get("result") == True

def test_boolean_inequality(interpreter):
    source = '{ result = true != false }'
    run_program(source, interpreter)
    assert interpreter.variables.get("result") == True

def test_numeric_comparison(interpreter):
    source = '{ result = (5 < 10) }'
    run_program(source, interpreter)
    assert interpreter.variables.get("result") == True

def test_unary_not(interpreter):
    source = '{ result = !true }'
    run_program(source, interpreter)
    assert interpreter.variables.get("result") == False

def test_complex_boolean_expression(interpreter):
    # Breakdown: 5-4 = 1; 3*2 = 6; 1 > 6 is false; !false is true; false == true is false; !false is true.
    source = '{ result = !(5 - 4 > 3 * 2 == !false) }'
    run_program(source, interpreter)
    assert interpreter.variables.get("result") == True

# ---------------------------
# Stage 3: Text Values Tests
# ---------------------------

def test_string_concatenation(interpreter):
    source = '{ s = "hello" + " " + "world" }'
    run_program(source, interpreter)
    assert interpreter.variables.get("s") == "hello world"

def test_string_equality(interpreter):
    source = '{ result = ("foo" + "bar") == "foobar" }'
    run_program(source, interpreter)
    assert interpreter.variables.get("result") == True

def test_string_inequality(interpreter):
    source = '{ result = "10 corgis" != "10" + "corgis" }'
    run_program(source, interpreter)
    assert interpreter.variables.get("result") == True

# ---------------------------
# Stage 4: Global Data Tests
# ---------------------------

def test_global_variable_assignment(interpreter):
    source = '''{
        x = 10
        x = x + 5
        y = x * 2
    }'''
    run_program(source, interpreter)
    assert interpreter.variables.get("x") == 15
    assert interpreter.variables.get("y") == 30

# ---------------------------
# Stage 5: Control Flow Tests
# ---------------------------

def test_while_loop(interpreter):
    source = '''{
        i = 0
        while i < 3 {
            i = i + 1
        }
    }'''
    run_program(source, interpreter)
    assert interpreter.variables.get("i") == 3

def test_nested_while_loops(interpreter):
    source = '''{
    i = 0
    while i < 3 {
        j = 0
        while j < 2 {
            print "i:" + i + " j:" + j
            j = j + 1
        }
        i = i + 1
    }
    }'''
    run_program(source, interpreter)
    assert interpreter.variables.get("i") == 3


# Run the tests with: pytest test_interpreter.py
if __name__ == '__main__':
    pytest.main()
