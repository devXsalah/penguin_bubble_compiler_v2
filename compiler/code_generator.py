# compiler/code_generator.py

"""
code_generator.py

Purpose:
Translates the list of tokens into Python code, handling structure and indentation
of the generated code.

Explanation:
- penguinDo        -> Python 'def' function definitions
- penguinSay       -> Python 'print(...)'
- penguinTake      -> Python 'dynamic_input(...)'
- returnIce        -> Python 'return ...' with operator replacements
- keepWalking      -> Python 'while <condition>:'
- penguinIf        -> Python 'if <condition>:'
- penguinWhatAbout -> Python 'elif <condition>:'
- penguinElse      -> Python 'else:'
- PENGUIN_BREAK    -> Python 'break'
- slideUp, slideDown, penguinBoost, givePenguins, snowball -> Arithmetic ops

Indentation:
- We use indent_code from utils.py to handle indentation based on the current level.
"""

from compiler.tokens import TokenType
from compiler.utils import indent_code

class CodeGenerator:
    def __init__(self):
        self.indentation_level = 0
        self.indentation_str = "    "  # Four spaces per indentation level

    def compile_tokens(self, tokens):
        """
        Compiles a list of tokens into lines of Python code.
        Returns a list of strings (each a line of Python code).
        """
        compiled_code = []

        for token in tokens:
            ttype = token["type"]

            # -------------------------------------------
            # 1) Function Definition (penguinDo)
            # -------------------------------------------
            if ttype == TokenType.PENGUIN_DO:
                # Example output:  def addOperation(x, y):
                line = f'def {token["name"]}({token["params"]}):'
                compiled_code.append(
                    indent_code(line, level=self.indentation_level, indent_str=self.indentation_str)
                )

                # Increase indentation for the function body
                self.indentation_level += 1
                block_code = self.compile_tokens(token["block"])
                compiled_code.extend(block_code)
                # Decrease indentation after function body
                self.indentation_level -= 1

            # -------------------------------------------
            # 2) Print Statements (penguinSay)
            # -------------------------------------------
            elif ttype == TokenType.PENGUIN_SAY:
                # Example output:  print("Hello World")
                line = f'print({token["value"]})'
                compiled_code.append(
                    indent_code(line, level=self.indentation_level, indent_str=self.indentation_str)
                )

            # -------------------------------------------
            # 3) Input (penguinTake)
            # -------------------------------------------
            elif ttype == TokenType.PENGUIN_TAKE:
                # Example output:  choice = dynamic_input("Enter your choice: ")
                line = f'{token["name"]} = dynamic_input({token["prompt"]})'
                compiled_code.append(
                    indent_code(line, level=self.indentation_level, indent_str=self.indentation_str)
                )

            # -------------------------------------------
            # 4) Return Statements (returnIce)
            # -------------------------------------------
            elif ttype == TokenType.RETURN_ICE:
                # Replace custom operators in the value
                expression = self._replace_custom_ops(token["value"])
                # Example output:  return x + y
                line = f'return {expression}'
                compiled_code.append(
                    indent_code(line, level=self.indentation_level, indent_str=self.indentation_str)
                )

            # -------------------------------------------
            # 5) Control Structures (while/if/elif/else)
            # -------------------------------------------
            elif ttype in [
                TokenType.KEEP_WALKING,
                TokenType.PENGUIN_IF,
                TokenType.PENGUIN_WHAT_ABOUT,
                TokenType.PENGUIN_ELSE
            ]:
                control_block = self._compile_control_structure(token)
                compiled_code.extend(control_block)

            # -------------------------------------------
            # 6) Arithmetic Operations
            #    (slideUp, slideDown, penguinBoost, givePenguins, snowball)
            # -------------------------------------------
            elif ttype in [
                TokenType.SLIDE_UP,
                TokenType.SLIDE_DOWN,
                TokenType.PENGUIN_BOOST,
                TokenType.GIVE_PENGUINS,
                TokenType.SNOWBALL
            ]:
                # Replace custom operators in the expression
                expression = self._replace_custom_ops(token["expression"])
                # Example output:  result = num1 + num2
                line = f'{token["target"]} = {expression}'
                compiled_code.append(
                    indent_code(line, level=self.indentation_level, indent_str=self.indentation_str)
                )

            # -------------------------------------------
            # 7) Break Statements (penguinBreak)
            # -------------------------------------------
            elif ttype == TokenType.PENGUIN_BREAK:
                # Example output:  break
                line = 'break'
                compiled_code.append(
                    indent_code(line, level=self.indentation_level, indent_str=self.indentation_str)
                )

            else:
                # Unrecognized tokens can be ignored or raise an error
                pass

        return compiled_code

    def _compile_control_structure(self, token):
        """
        Compiles control structures: keepWalking (while), penguinIf (if),
        penguinWhatAbout (elif), penguinElse (else).
        Adjusts indentation levels appropriately.
        """
        compiled_control = []
        ttype = token["type"]

        if ttype == TokenType.KEEP_WALKING:
            # while <condition>:
            keyword = "while"
            condition = token.get("condition", "").strip()
            header_line = f'{keyword} {condition}:'
            compiled_control.append(
                indent_code(header_line, level=self.indentation_level, indent_str=self.indentation_str)
            )
            # Increase indentation for the block
            self.indentation_level += 1
            block_code = self.compile_tokens(token["block"])
            compiled_control.extend(block_code)
            # Decrease indentation after block
            self.indentation_level -= 1

        elif ttype == TokenType.PENGUIN_IF:
            # if <condition>:
            keyword = "if"
            condition = token.get("condition", "").strip()
            header_line = f'{keyword} {condition}:'
            compiled_control.append(
                indent_code(header_line, level=self.indentation_level, indent_str=self.indentation_str)
            )
            # Increase indentation for the block
            self.indentation_level += 1
            block_code = self.compile_tokens(token["block"])
            compiled_control.extend(block_code)
            # Decrease indentation after block
            self.indentation_level -= 1

        elif ttype == TokenType.PENGUIN_WHAT_ABOUT:
            # elif <condition>:
            keyword = "elif"
            condition = token.get("condition", "").strip()
            header_line = f'{keyword} {condition}:'
            compiled_control.append(
                indent_code(header_line, level=self.indentation_level, indent_str=self.indentation_str)
            )
            # Increase indentation for the block
            self.indentation_level += 1
            block_code = self.compile_tokens(token["block"])
            compiled_control.extend(block_code)
            # Decrease indentation after block
            self.indentation_level -= 1

        elif ttype == TokenType.PENGUIN_ELSE:
            # else:
            keyword = "else"
            header_line = f'{keyword}:'
            compiled_control.append(
                indent_code(header_line, level=self.indentation_level, indent_str=self.indentation_str)
            )
            # Increase indentation for the block
            self.indentation_level += 1
            block_code = self.compile_tokens(token["block"])
            compiled_control.extend(block_code)
            # Decrease indentation after block
            self.indentation_level -= 1

        return compiled_control

    def _replace_custom_ops(self, expression):
        """
        Replaces any inline custom operations (slideUp, slideDown, penguinBoost,
        givePenguins, snowball) in the 'expression' string with their Python equivalents.
        This is a naive string replacement approach.
        """
        replacements = {
            "slideUp": "+",
            "slideDown": "-",
            "penguinBoost": "*",
            "givePenguins": "/",
            "snowball": "**"
        }

        for custom_op, py_op in replacements.items():
            expression = expression.replace(custom_op, py_op)

        return expression
