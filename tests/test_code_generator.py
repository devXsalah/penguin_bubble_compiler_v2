#Purpose: 
# Tests the functionality of the code generator to ensure tokens are correctly translated into Python code.

"""
Explanation:

Test Cases:

test_compile_penguin_say: Ensures penguinSay is translated to print().
test_compile_penguin_take: Checks penguinTake is handled using dynamic_input.
test_compile_variable_assignment: Verifies variable assignments.
test_compile_return_ice: Tests returnIce translation.
test_compile_penguin_do: Ensures function definitions are correctly translated.
test_compile_keep_walking: Tests keepWalking (while loop) translation.
test_compile_penguin_if_else: Checks if-else statement translation.
test_compile_complex_structure: Tests a complex compilation involving multiple constructs.
"""
import unittest
from compiler.code_generator import CodeGenerator

class TestCodeGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = CodeGenerator()

    def test_compile_penguin_say(self):
        tokens = [{"type": "penguinSay", "value": '"Hello, World!"'}]
        compiled = self.generator.compile_tokens(tokens)
        expected = ['print("Hello, World!")']
        self.assertEqual(compiled, expected)

    def test_compile_penguin_take(self):
        tokens = [{"type": "penguinTake", "name": "name", "prompt": '"Enter your name:"'}]
        compiled = self.generator.compile_tokens(tokens)
        expected = ['name = dynamic_input("Enter your name:")']
        self.assertEqual(compiled, expected)

    def test_compile_variable_assignment(self):
        tokens = [{"type": "variableAssignment", "name": "x", "value": "10"}]
        compiled = self.generator.compile_tokens(tokens)
        expected = ['x = 10']
        self.assertEqual(compiled, expected)

    def test_compile_return_ice(self):
        tokens = [{"type": "returnIce", "value": "result"}]
        compiled = self.generator.compile_tokens(tokens)
        expected = ['return result']
        self.assertEqual(compiled, expected)

    def test_compile_penguin_do(self):
        tokens = [{
            "type": "penguinDo",
            "name": "add",
            "params": "a, b",
            "block": [
                {"type": "penguinSay", "value": '"Adding numbers"'},
                {"type": "variableAssignment", "name": "result", "value": "a + b"},
                {"type": "returnIce", "value": "result"}
            ]
        }]
        compiled = self.generator.compile_tokens(tokens)
        expected = [
            "def add(a, b):",
            "    print(\"Adding numbers\")",
            "    result = a + b",
            "    return result"
        ]
        self.assertEqual(compiled, expected)

    def test_compile_keep_walking(self):
        tokens = [{
            "type": "keepWalking",
            "condition": "x < 30",
            "block": [
                {"type": "penguinSay", "value": '"Age is less than 30."'},
                {"type": "variableAssignment", "name": "x", "value": "x + 1"}
            ]
        }]
        compiled = self.generator.compile_tokens(tokens)
        expected = [
            "while x < 30:",
            "    print(\"Age is less than 30.\")",
            "    x = x + 1"
        ]
        self.assertEqual(compiled, expected)

    def test_compile_penguin_if_else(self):
        tokens = [
            {
                "type": "penguinIf",
                "condition": "x == z",
                "block": [
                    {"type": "penguinSay", "value": '"x now equals z"'}
                ]
            },
            {
                "type": "penguinElse",
                "block": [
                    {"type": "penguinSay", "value": '"x does not equal z"'}
                ]
            }
        ]
        compiled = self.generator.compile_tokens(tokens)
        expected = [
            "if x == z:",
            "    print(\"x now equals z\")",
            "else:",
            "    print(\"x does not equal z\")"
        ]
        self.assertEqual(compiled, expected)

    def test_compile_complex_structure(self):
        tokens = [
            {"type": "penguinSay", "value": '"Hello, World!"'},
            {"type": "variableAssignment", "name": "x", "value": "10"},
            {"type": "variableAssignment", "name": "y", "value": "20"},
            {
                "type": "penguinDo",
                "name": "add",
                "params": "a, b",
                "block": [
                    {"type": "penguinSay", "value": '"Adding numbers"'},
                    {"type": "variableAssignment", "name": "result", "value": "a + b"},
                    {"type": "returnIce", "value": "result"}
                ]
            },
            {"type": "variableAssignment", "name": "z", "value": "add(x, y)"},
            {
                "type": "keepWalking",
                "condition": "x < z",
                "block": [
                    {"type": "penguinSay", "value": '"x is still less than z"'},
                    {"type": "variableAssignment", "name": "x", "value": "x + 1"}
                ]
            },
            {
                "type": "penguinIf",
                "condition": "x == z",
                "block": [
                    {"type": "penguinSay", "value": '"x now equals z"'}
                ]
            },
            {
                "type": "penguinElse",
                "block": [
                    {"type": "penguinSay", "value": '"x does not equal z"'}
                ]
            }
        ]
        compiled = self.generator.compile_tokens(tokens)
        expected = [
            'print("Hello, World!")',
            'x = 10',
            'y = 20',
            "def add(a, b):",
            "    print(\"Adding numbers\")",
            "    result = a + b",
            "    return result",
            'z = add(x, y)',
            "while x < z:",
            "    print(\"x is still less than z\")",
            "    x = x + 1",
            "if x == z:",
            "    print(\"x now equals z\")",
            "else:",
            "    print(\"x does not equal z\")"
        ]
        self.assertEqual(compiled, expected)

if __name__ == '__main__':
    unittest.main()
