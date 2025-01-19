#Purpose: 
# Translates the list of tokens into Python code, 
# handling the structure and indentation of the generated code.

"""
Explanation:

Function Definitions (penguinDo): Translates to Python def statements with proper indentation.
Print Statements (penguinSay): Translates to Python print() functions.
Variable Assignments: Directly translates to Python assignments.
Input Handling (penguinTake): Utilizes a dynamic_input function (defined separately) for user inputs.
Return Statements (returnIce): Translates to Python return statements.
Control Structures:
KEEP_WALKING: Translates to while loops.
PENGUIN_IF, PENGUIN_WHAT_ABOUT, PENGUIN_ELSE: Translate to if, elif, and else statements respectively.
Indentation: Ensures that nested blocks are properly indented using four spaces.

"""

# compiler/code_generator.py
from compiler.tokens import TokenType
from compiler.utils import indent_code

class CodeGenerator:
    def __init__(self):
        pass  # No initialization needed for now

    def compile_tokens(self, tokens):
        compiled_code = []
        for token in tokens:
            if token["type"] == TokenType.PENGUIN_DO:
                # Compile function definitions
                function_code = f'def {token["name"]}({token["params"]}):\n'
                block_code = self.compile_tokens(token["block"])
                # Indent the function body with 4 spaces
                block_code = '\n'.join(['    ' + line for line in block_code])
                function_code += block_code
                compiled_code.append(function_code)
            elif token["type"] == TokenType.PENGUIN_SAY:
                compiled_code.append(f'print({token["value"]})')
            elif token["type"] == TokenType.VARIABLE_ASSIGNMENT:
                compiled_code.append(f'{token["name"]} = {token["value"]}')
            elif token["type"] == TokenType.PENGUIN_TAKE:
                # Use the dynamic_input function instead of specifying the data type
                compiled_code.append(f'{token["name"]} = dynamic_input({token["prompt"]})')
            elif token["type"] == TokenType.RETURN_ICE:
                compiled_code.append(f'return {token["value"]}')
            elif token["type"] in [TokenType.KEEP_WALKING, TokenType.PENGUIN_IF, TokenType.PENGUIN_WHAT_ABOUT, TokenType.PENGUIN_ELSE]:
                # Handle control structures
                if token["type"] == TokenType.KEEP_WALKING:
                    keyword = "while"
                elif token["type"] == TokenType.PENGUIN_IF:
                    keyword = "if"
                elif token["type"] == TokenType.PENGUIN_WHAT_ABOUT:
                    keyword = "elif"
                elif token["type"] == TokenType.PENGUIN_ELSE:
                    keyword = "else"
                
                if keyword != "else":
                    condition = token["condition"]
                    header = f'{keyword} {condition}:'
                else:
                    header = f'{keyword}:'
                
                block_code = self.compile_tokens(token["block"])
                block_code = '\n'.join(['    ' + line for line in block_code])
                compiled_code.append(f'{header}\n{block_code}')
            else:
                # Handle other token types or ignore
                pass
        return compiled_code
