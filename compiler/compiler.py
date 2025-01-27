"""

Purpose:
Integrates the tokenizer, parser, and code generator to perform the full compilation process,
transforming .pg source code into Python code.

Explanation:
1. The Tokenizer converts the raw .pg source code into a structured list of tokens.
2. The Parser validates the tokens to ensure syntax correctness.
3. The CodeGenerator translates the validated tokens into equivalent Python code.
4. The compiler injects a 'dynamic_input' function at the top of the generated Python code
   to handle user input dynamically with appropriate type conversion.
"""

from compiler.tokenizer import Tokenizer
from compiler.parser import Parser
from compiler.code_generator import CodeGenerator

class PenguinBubbleCompiler:
    def __init__(self):
        # Initialize the Tokenizer, Parser, and CodeGenerator components
        self.tokenizer = Tokenizer()
        self.parser = Parser()
        self.code_generator = CodeGenerator()

    def compile(self, code):
        """
        Orchestrates the compilation process from .pg code to Python code.

        :param code: The raw .pg source code.
        :return: The compiled Python code as a string.
        """

        # -------------------------------------------------------
        # Step 1: Tokenize the source code
        # Converts the raw .pg source code into a list of tokens
        # -------------------------------------------------------
        tokens = self.tokenizer.tokenize(code)

        # -------------------------------------------------------
        # Step 2: Parse the tokens to validate their syntax
        # Ensures all tokens follow the correct .pg syntax
        # -------------------------------------------------------
        try:
            self.parser.parse(tokens)
        except SyntaxError as e:
            # Print the syntax error and return an empty string if parsing fails
            print(f"Syntax Error: {e}")
            return ""

        # -------------------------------------------------------
        # Step 3: Prepare the compiled Python code
        # Initialize a list to hold all lines of the final Python code
        # -------------------------------------------------------
        compiled_code = []

        # -------------------------------------------------------
        # Step 4: Inject the dynamic_input function
        # This function is added at the top of the Python code to handle
        # user input with automatic type conversion to int, float, or string
        # -------------------------------------------------------
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

        # -------------------------------------------------------
        # Step 5: Generate Python code from validated tokens
        # Translate tokens into equivalent Python statements
        # -------------------------------------------------------
        compiled_code.extend(self.code_generator.compile_tokens(tokens))

        # Return the final Python code as a single string
        return '\n'.join(compiled_code)
