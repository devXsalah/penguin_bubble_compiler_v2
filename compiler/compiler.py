
"""
compiler.py

Purpose:
Integrates the tokenizer, parser, and code generator to perform the full compilation process,
transforming .pg code into Python code.

Explanation:
1. The Tokenizer converts the raw .pg source code into a list of tokens.
2. The Parser validates the tokens to ensure syntax correctness.
3. The CodeGenerator translates the validated tokens into Python code.
4. The compiler injects a 'dynamic_input' function at the top of the output Python code.
"""

from compiler.tokenizer import Tokenizer
from compiler.parser import Parser
from compiler.code_generator import CodeGenerator

class PenguinBubbleCompiler:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.parser = Parser()
        self.code_generator = CodeGenerator()

    def compile(self, code):
        # 1) Tokenize the source code
        tokens = self.tokenizer.tokenize(code)
        # 2) Parse the tokens to validate syntax
        try:
            self.parser.parse(tokens)
        except SyntaxError as e:
            print(f"Syntax Error: {e}")
            return ""

        # 3) Prepare the list that will hold all lines of the final Python code
        compiled_code = []

        # 4) Insert the dynamic_input function at the top of the compiled code
        dynamic_input_function = [
            "def dynamic_input(prompt):",
            "    inp = input(prompt)",
            "    try:",
            "        return int(inp)",
            "    except ValueError:",
            "        try:",
            "            return float(inp)",
            "        except ValueError:",
            "            return inp",
            ""
        ]
        compiled_code.extend(dynamic_input_function)

        print(tokens)


        compiled_code.extend(self.code_generator.compile_tokens(tokens))

        return '\n'.join(compiled_code)
