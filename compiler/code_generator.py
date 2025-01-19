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

class CodeGenerator:
    def __init__(self):
        self.indentation_level = 0
        self.indentation_str = "    "  # Four spaces per indentation level

    def compile_tokens(self, tokens):
        compiled_code = []
        for token in tokens:
            if token["type"] == TokenType.PENGUIN_DO:
                # Compile function definitions
                indent = self._get_indent()
                function_header = f'{indent}def {token["name"]}({token["params"]}):'
                compiled_code.append(function_header)
                
                # Increase indentation for the function body
                self.indentation_level += 1
                block_code = self.compile_tokens(token["block"])
                compiled_code.extend(block_code)
                self.indentation_level -= 1  # Reset indentation after function body

            elif token["type"] == TokenType.PENGUIN_SAY:
                indent = self._get_indent()
                print_statement = f'{indent}print({token["value"]})'
                compiled_code.append(print_statement)

            elif token["type"] == TokenType.VARIABLE_ASSIGNMENT:
                indent = self._get_indent()
                assignment = f'{indent}{token["name"]} = {token["value"]}'
                compiled_code.append(assignment)

            elif token["type"] == TokenType.PENGUIN_TAKE:
                indent = self._get_indent()
                input_statement = f'{indent}{token["name"]} = dynamic_input({token["prompt"]})'
                compiled_code.append(input_statement)

            elif token["type"] == TokenType.RETURN_ICE:
                indent = self._get_indent()
                return_statement = f'{indent}return {token["value"]}'
                compiled_code.append(return_statement)

            elif token["type"] in [TokenType.KEEP_WALKING, TokenType.PENGUIN_IF, TokenType.PENGUIN_WHAT_ABOUT, TokenType.PENGUIN_ELSE]:
                compiled_control = self._compile_control_structure(token)
                if compiled_control:
                    compiled_code.extend(compiled_control)

            else:
                # Handle other token types or ignore
                pass

        return compiled_code

    def _compile_control_structure(self, token):
        compiled_control = []
        keyword = ""
        condition = ""

        if token["type"] == TokenType.KEEP_WALKING:
            keyword = "while"
            condition = token.get("condition", "")
        elif token["type"] == TokenType.PENGUIN_IF:
            keyword = "if"
            condition = token.get("condition", "")
        elif token["type"] == TokenType.PENGUIN_WHAT_ABOUT:
            keyword = "elif"
            condition = token.get("condition", "")
        elif token["type"] == TokenType.PENGUIN_ELSE:
            keyword = "else"

        indent = self._get_indent()

        if keyword != "else":
            header = f'{indent}{keyword} {condition}:'
        else:
            # Decrease indentation before adding 'else:' to align with 'if'
            self.indentation_level = max(self.indentation_level - 1, 0)
            indent = self._get_indent()
            header = f'{indent}{keyword}:'

        compiled_control.append(header)

        if keyword != "else":
            # Increase indentation for the block under control structure
            self.indentation_level += 1
            block_code = self.compile_tokens(token["block"])
            compiled_control.extend(block_code)
            self.indentation_level -= 1
        else:
            # Increase indentation for the 'else' block
            self.indentation_level += 1
            block_code = self.compile_tokens(token["block"])
            compiled_control.extend(block_code)

        return compiled_control

    def _get_indent(self):
        """Returns the current indentation string based on the indentation level."""
        return self.indentation_str * self.indentation_level
