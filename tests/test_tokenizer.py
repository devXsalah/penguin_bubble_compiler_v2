#Purpose: 
# Tests the functionality of the tokenizer to ensure it correctly parses .pg code into tokens.

"""
Explanation:

Test Cases:

test_penguin_say: Verifies the parsing of penguinSay commands.
test_penguin_take_with_quotes & test_penguin_take_without_quotes: Tests penguinTake with and without quoted prompts.
test_variable_assignment: Checks variable assignments.
test_return_ice: Ensures returnIce is parsed correctly.
test_penguin_do: Tests function definitions.
test_keep_walking: Verifies keepWalking loops.
test_penguin_if_else: Tests if-else statements.
test_custom_arithmetic_operations: Checks custom arithmetic operations mapping.
test_unrecognized_syntax: Ensures unrecognized commands are skipped.
"""
import unittest
from compiler.tokenizer import Tokenizer

class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer()

    def test_penguin_say(self):
        code = 'penguinSay "Hello, World!"'
        tokens = self.tokenizer.tokenize(code)
        expected = [{"type": "penguinSay", "value": '"Hello, World!"'}]
        self.assertEqual(tokens, expected)

    def test_penguin_take_with_quotes(self):
        code = 'penguinTake(name) "Enter your name:"'
        tokens = self.tokenizer.tokenize(code)
        expected = [{"type": "penguinTake", "name": "name", "prompt": '"Enter your name:"'}]
        self.assertEqual(tokens, expected)

    def test_penguin_take_without_quotes(self):
        code = 'penguinTake(age) Enter your age:'
        tokens = self.tokenizer.tokenize(code)
        expected = [{"type": "penguinTake", "name": "age", "prompt": "Enter your age:"}]
        self.assertEqual(tokens, expected)

    def test_variable_assignment(self):
        code = 'x = 10'
        tokens = self.tokenizer.tokenize(code)
        expected = [{"type": "variableAssignment", "name": "x", "value": "10"}]
        self.assertEqual(tokens, expected)

    def test_return_ice(self):
        code = 'returnIce x + y'
        tokens = self.tokenizer.tokenize(code)
        expected = [{"type": "returnIce", "value": "x + y"}]
        self.assertEqual(tokens, expected)

    def test_penguin_do(self):
        code = """
penguinDo add(a, b)
    penguinSay "Adding numbers"
    result = a + b
    returnIce result
"""
        tokens = self.tokenizer.tokenize(code)
        expected = [{
            "type": "penguinDo",
            "name": "add",
            "params": "a, b",
            "block": [
                {"type": "penguinSay", "value": '"Adding numbers"'},
                {"type": "variableAssignment", "name": "result", "value": "a + b"},
                {"type": "returnIce", "value": "result"}
            ]
        }]
        self.assertEqual(tokens, expected)

    def test_keep_walking(self):
        code = """
keepWalking(x < 30)
    penguinSay "Age is less than 30."
    x = x + 1
"""
        tokens = self.tokenizer.tokenize(code)
        expected = [{
            "type": "keepWalking",
            "condition": "x < 30",
            "block": [
                {"type": "penguinSay", "value": '"Age is less than 30."'},
                {"type": "variableAssignment", "name": "x", "value": "x + 1"}
            ]
        }]
        self.assertEqual(tokens, expected)

    def test_penguin_if_else(self):
        code = """
penguinIf(x == z)
    penguinSay "x equals z"
penguinElse
    penguinSay "x does not equal z"
"""
        tokens = self.tokenizer.tokenize(code)
        expected = [
            {
                "type": "penguinIf",
                "condition": "x == z",
                "block": [
                    {"type": "penguinSay", "value": '"x equals z"'}
                ]
            },
            {
                "type": "penguinElse",
                "block": [
                    {"type": "penguinSay", "value": '"x does not equal z"'}
                ]
            }
        ]
        self.assertEqual(tokens, expected)

    def test_custom_arithmetic_operations(self):
        code = 'slideUp(total) = x + y'
        tokens = self.tokenizer.tokenize(code)
        expected = [{"type": "variableAssignment", "name": "total", "value": "x + y"}]
        self.assertEqual(tokens, expected)

    def test_unrecognized_syntax(self):
        code = 'unknownCommand "test"'
        tokens = self.tokenizer.tokenize(code)
        expected = []  # Should skip unrecognized syntax
        self.assertEqual(tokens, expected)

if __name__ == '__main__':
    unittest.main()
