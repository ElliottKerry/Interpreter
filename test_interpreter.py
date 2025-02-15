# test_interpreter.py
# This file contains tests for the interpreter. It uses pytest to run the tests.
# Unit tests are useful to ensure that the interpreter works as expected.

import pytest
import io
import sys
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

def test_assignment(interpreter):
    source = '{ i = 5 }'
    run_program(source, interpreter)
    # Check that variable 'i' was set correctly.
    assert interpreter.variables.get("i") == 5

def test_addition(interpreter):
    source = '{ i = 5 + 3 }'
    run_program(source, interpreter)
    assert interpreter.variables.get("i") == 8

def test_nested_loop(interpreter):
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

# You can run this file with `pytest test_interpreter.py`
if __name__ == '__main__':
    pytest.main()
