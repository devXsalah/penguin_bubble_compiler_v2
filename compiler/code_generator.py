
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

"""
from compiler.tokens import TokenType


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
                    (token["indent"]*" ")+line
                )

            # -------------------------------------------
            # 2) Print Statements (penguinSay)
            # -------------------------------------------
            elif ttype == TokenType.PENGUIN_SAY:
                # Example output:  print("Hello World")
                line = f'print({token["value"]})'
                compiled_code.append(
                    (token["indent"]*" ")+line
                )

            # -------------------------------------------
            # 3) Input (penguinTake)
            # -------------------------------------------
            elif ttype == TokenType.PENGUIN_TAKE:
                # Example output:  choice = dynamic_input("Enter your choice: ")
                line = f'{token["name"]} = dynamic_input({token["prompt"]})'
                compiled_code.append(
                    (token["indent"]*" ")+line
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
                    (token["indent"]*" ")+line
                )

            # -------------------------------------------
            # 4) Var statement (iceBucket)
            # -------------------------------------------
            elif ttype == TokenType.ICE_BUCKET:
                # Replace custom operators in the value
                expression = self._replace_custom_ops(token["value"])
                # Example output:  return x + y
                line = f'{expression}'
                compiled_code.append(
                    (token["indent"]*" ")+line
                )
                
            # -------------------------------------------
            # 5) Control Structures (while/if/elif/else)
            # -------------------------------------------
            elif ttype == TokenType.KEEP_WALKING:
                # while <condition>:
                keyword = "while"
                condition = token.get("condition", "").strip()
                header_line = f'{keyword} {condition}:'
                compiled_code.append(
                    (token["indent"]*" ")+ header_line
                )
            
            elif ttype == TokenType.PENGUIN_IF:
                # while <condition>:
                keyword = "if"
                condition = token.get("condition", "").strip()
                header_line = f'{keyword} {condition}:'
                compiled_code.append(
                    (token["indent"]*" ")+ header_line
                )
                
            elif ttype == TokenType.PENGUIN_WHAT_ABOUT:
                # while <condition>:
                keyword = "elif"
                condition = token.get("condition", "").strip()
                header_line = f'{keyword} {condition}:'
                compiled_code.append(
                    (token["indent"]*" ")+ header_line
                )
                
            elif ttype == TokenType.PENGUIN_ELSE:
                # while <condition>:
                keyword = "else"
                condition = token.get("condition", "").strip()
                header_line = f'{keyword} {condition}:'
                compiled_code.append(
                    (token["indent"]*" ")+ header_line
                )
            
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
                    (token["indent"]*" ")+line
                )

            else:
                # Unrecognized tokens can be ignored or raise an error
                pass

        return compiled_code


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
