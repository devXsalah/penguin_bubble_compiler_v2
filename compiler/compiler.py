#Purpose: 
# Integrates the tokenizer and code generator to perform the full compilation process, 
# transforming .pg code into Python code.

"""
Explanation:

Initialization:
Tokenizer Instance: Responsible for converting raw .pg code into tokens.
CodeGenerator Instance: Handles the transformation of tokens into Python code.
Compilation Process (compile Method):
Tokenization: Converts the raw code into tokens using the Tokenizer.
Dynamic Input Function: Inserts a helper function dynamic_input at the beginning of the generated Python code to handle user inputs.
Token Separation: Separates function definitions (penguinDo) from other tokens to ensure that functions are defined before they are called.
Code Generation: Uses the CodeGenerator to translate tokens into Python code, compiling functions first and then other statements.
Output: Joins all compiled code lines into a single string for output.
"""

from compiler.tokenizer import Tokenizer
from compiler.code_generator import CodeGenerator

class PenguinBubbleCompiler:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.code_generator = CodeGenerator()

    def compile(self, code):
        tokens = self.tokenizer.tokenize(code)
        compiled_code = []

        # Add the dynamic_input function at the top of the compiled code
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

        # Separate function tokens and other tokens
        function_tokens = [token for token in tokens if token["type"] == "penguinDo"]
        other_tokens = [token for token in tokens if token["type"] != "penguinDo"]

        # Compile function tokens first
        compiled_code.extend(self.code_generator.compile_tokens(function_tokens))

        # Then compile other tokens
        compiled_code.extend(self.code_generator.compile_tokens(other_tokens))

        return '\n'.join(compiled_code)
