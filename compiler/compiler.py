#Purpose: 
# Integrates the tokenizer and code generator to perform the full compilation process, 
# transforming .pg code into Python code.

"""
    Explanation:

    The CodeGenerator is responsible for translating a list of structured tokens into properly indented Python code. It handles various token types by mapping them to their corresponding Python syntax, ensuring that control structures are correctly indented to reflect their hierarchical relationships.

    Key Functionalities:

    1. **Function Definitions (`PENGUIN_DO`):**
       - Translates to Python `def` statements.
       - Manages indentation levels to ensure the function body is properly indented.
       - Supports nested function definitions if required.

    2. **Print Statements (`PENGUIN_SAY`):**
       - Translates to Python `print()` functions.
       - Ensures that print statements within control structures are correctly indented.

    3. **Variable Assignments (`VARIABLE_ASSIGNMENT`):**
       - Directly translates to Python variable assignments.
       - Handles assignments both within and outside control structures.

    4. **Input Handling (`PENGUIN_TAKE`):**
       - Utilizes a pre-defined `dynamic_input` function to handle user inputs.
       - Translates to Python assignments that call `dynamic_input()` with the provided prompt.

    5. **Return Statements (`RETURN_ICE`):**
       - Translates to Python `return` statements.
       - Ensures proper indentation within function bodies.

    6. **Control Structures:**
       - **While Loops (`KEEP_WALKING`):** Translates to Python `while` loops.
       - **If Statements (`PENGUIN_IF`):** Translates to Python `if` statements.
       - **Elif Statements (`PENGUIN_WHAT_ABOUT`):** Translates to Python `elif` statements.
       - **Else Statements (`PENGUIN_ELSE`):** Translates to Python `else` statements.
       - Manages indentation levels dynamically to reflect nested blocks within these structures.

    7. **Indentation Management:**
       - Maintains an `indentation_level` to track the current depth of nested blocks.
       - Uses a consistent indentation string (`self.indentation_str`) to ensure uniformity across the generated code.
       - Adjusts indentation levels when entering and exiting control structures and function definitions.

    8. **Extensibility:**
       - Designed to easily incorporate additional token types and their corresponding Python translations.
       - Facilitates maintenance and scalability as new features are added to the `.pg` language.

    9. **Error Handling:**
       - Currently, unrecognized tokens are ignored. This can be enhanced to include logging or raising exceptions for better debugging and feedback.
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
