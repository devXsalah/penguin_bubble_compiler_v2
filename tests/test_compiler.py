#
# Purpose: Tests the overall compilation process, 
# ensuring that the tokenizer and code generator work together seamlessly.

"""
Explanation:

Test Cases:

test_compile_simple_script: Tests the compilation of a simple penguinSay command.
test_compile_full_script: Tests the compilation of a full script containing various commands and control structures.
test_compile_with_custom_arithmetic_operations: Ensures custom arithmetic operations like slideUp are correctly translated.
test_compile_with_unrecognized_syntax: Checks that unrecognized commands are skipped without affecting the rest of the compilation.
"""

import unittest
from compiler.compiler import PenguinBubbleCompiler

class TestCompiler(unittest.TestCase):
    def setUp(self):
        self.compiler = PenguinBubbleCompiler()

    def test_compile_simple_script(self):
        code = 'penguinSay "Hello, World!"'
        compiled = self.compiler.compile(code)
        expected = '\n'.join([
            "def dynamic_input(prompt):",
            "    inp = input(prompt)",
            "    try:",
            "        return int(inp)",
            "    except ValueError:",
            "        try:",
            "            return float(inp)",
            "        except ValueError:",
            "            return inp",
            "",
            'print("Hello, World!")'
        ])
        self.assertMultiLineEqual(compiled, expected)

    def test_compile_full_script(self):
        code = """
penguinSay "Hello, World!"
x = 10
y = 20
z = add(x, y)
KEEP_WALKING x < z
    penguinSay "x is still less than z"
    x = x + 1
PENGUIN_IF x == z
    penguinSay "x now equals z"
PENGUIN_ELSE
    penguinSay "x does not equal z"
"""
        compiled = self.compiler.compile(code)
        expected = '\n'.join([
            "def dynamic_input(prompt):",
            "    inp = input(prompt)",
            "    try:",
            "        return int(inp)",
            "    except ValueError:",
            "        try:",
            "            return float(inp)",
            "        except ValueError:",
            "            return inp",
            "",
            'print("Hello, World!")',
            "x = 10",
            "y = 20",
            "z = add(x, y)",
            "while x < z:",
            '    print("x is still less than z")',
            "    x = x + 1",
            "if x == z:",
            '    print("x now equals z")',
            "else:",
            '    print("x does not equal z")'
        ])
        self.assertMultiLineEqual(compiled, expected)

    def test_compile_with_custom_arithmetic_operations(self):
        code = 'slideUp(total) = x + y'
        compiled = self.compiler.compile(code)
        expected = '\n'.join([
            "def dynamic_input(prompt):",
            "    inp = input(prompt)",
            "    try:",
            "        return int(inp)",
            "    except ValueError:",
            "        try:",
            "            return float(inp)",
            "        except ValueError:",
            "            return inp",
            "",
            'total = x + y'
        ])
        self.assertMultiLineEqual(compiled, expected)

    def test_compile_with_unrecognized_syntax(self):
        code = """
penguinSay "Hello, World!"
unknownCommand "This should be skipped"
x = 10
"""
        compiled = self.compiler.compile(code)
        expected = '\n'.join([
            "def dynamic_input(prompt):",
            "    inp = input(prompt)",
            "    try:",
            "        return int(inp)",
            "    except ValueError:",
            "        try:",
            "            return float(inp)",
            "        except ValueError:",
            "            return inp",
            "",
            'print("Hello, World!")',
            "x = 10"
        ])
        self.assertMultiLineEqual(compiled, expected)

if __name__ == '__main__':
    unittest.main()
