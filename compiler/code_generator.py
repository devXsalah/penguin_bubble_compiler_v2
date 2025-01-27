"""
Purpose:
Generates Python code from a list of tokens, handling syntax, structure, and indentation.

Explanation:
- penguinDo        -> Generates Python function definitions (def ...).
- penguinSay       -> Translates to Python 'print(...)' statements.
- penguinTake      -> Maps to 'dynamic_input(...)' for user input.
- returnIce        -> Compiles to Python 'return ...' with custom operator replacements.
- keepWalking      -> Converts to Python 'while <condition>:' loops.
- penguinIf        -> Translates to Python 'if <condition>:' statements.
- penguinWhatAbout -> Maps to Python 'elif <condition>:'.
- penguinElse      -> Converts to Python 'else:' blocks.
- breakIce         -> Produces Python 'break'.
- slideUp, slideDown, penguinBoost, givePenguins, snowball -> Custom arithmetic operations.

Additional Functionality:
Handles custom operators (e.g., slideUp, snowball) by replacing them with equivalent Python operators.
"""

from compiler.tokens import TokenType

class CodeGenerator:
    def __init__(self):
        # Tracks current indentation level and defines indentation as four spaces
        self.indentation_level = 0
        self.indentation_str = "    "

    def compile_tokens(self, tokens):
        """
        Compiles a list of tokens into Python code.
        Returns a list of strings where each string represents a line of Python code.
        """
        compiled_code = []

        for token in tokens:
            ttype = token["type"]

            # -------------------------------------------
            # 1) Function Definition (penguinDo -> def)
            # Example: def function_name(params):
            # -------------------------------------------
            if ttype == TokenType.PENGUIN_DO:
                line = f'def {token["name"]}({token["params"]}):'
                compiled_code.append((token["indent"] * " ") + line)

            # -------------------------------------------
            # 2) Print Statements (penguinSay -> print)
            # Example: print("Hello World")
            # -------------------------------------------
            elif ttype == TokenType.PENGUIN_SAY:
                line = f'print({token["value"]})'
                compiled_code.append((token["indent"] * " ") + line)

            # -------------------------------------------
            # 3) Input Handling (penguinTake -> dynamic_input)
            # Example: variable = dynamic_input("Enter value:")
            # -------------------------------------------
            elif ttype == TokenType.PENGUIN_TAKE:
                line = f'{token["name"]} = dynamic_input({token["prompt"]})'
                compiled_code.append((token["indent"] * " ") + line)

            # -------------------------------------------
            # 4) Return Statements (returnIce -> return)
            # Example: return x + y
            # -------------------------------------------
            elif ttype == TokenType.RETURN_ICE:
                expression = self._replace_custom_ops(token["value"])
                line = f'return {expression}'
                compiled_code.append((token["indent"] * " ") + line)

            # -------------------------------------------
            # 5) Break Statements (breakIce -> break)
            # Example: break
            # -------------------------------------------
            elif ttype == TokenType.BREAKICE:
                compiled_code.append((token["indent"] * " ") + "break")

            # -------------------------------------------
            # 6) Variable Assignment (iceBucket)
            # Example: variable = value
            # -------------------------------------------
            elif ttype == TokenType.ICE_BUCKET:
                expression = self._replace_custom_ops(token["value"])
                line = expression
                compiled_code.append((token["indent"] * " ") + line)

            # -------------------------------------------
            # 7) Control Structures (while/if/elif/else)
            # - keepWalking -> while <condition>:
            # - penguinIf   -> if <condition>:
            # - penguinWhatAbout -> elif <condition>:
            # - penguinElse -> else:
            # -------------------------------------------
            elif ttype in [TokenType.KEEP_WALKING, TokenType.PENGUIN_IF, TokenType.PENGUIN_WHAT_ABOUT, TokenType.PENGUIN_ELSE]:
                keyword_map = {
                    TokenType.KEEP_WALKING: "while",
                    TokenType.PENGUIN_IF: "if",
                    TokenType.PENGUIN_WHAT_ABOUT: "elif",
                    TokenType.PENGUIN_ELSE: "else :"
                }
                keyword = keyword_map[ttype]
                condition = token.get("condition", "").strip()
                header_line = f'{keyword} {condition}:'.rstrip(":")
                if ttype != TokenType.PENGUIN_ELSE:
                    header_line += ":"
                compiled_code.append((token["indent"] * " ") + header_line)

            # -------------------------------------------
            # 8) Arithmetic Operations
            # Custom operators replaced with Python equivalents.
            # Example: result = num1 + num2
            # -------------------------------------------
            elif ttype in [
                TokenType.SLIDE_UP,
                TokenType.SLIDE_DOWN,
                TokenType.PENGUIN_BOOST,
                TokenType.GIVE_PENGUINS,
                TokenType.SNOWBALL
            ]:
                expression = self._replace_custom_ops(token["expression"])
                line = f'{token["target"]} = {expression}'
                compiled_code.append((token["indent"] * " ") + line)

            # -------------------------------------------
            # 9) Ignore Unrecognized Tokens
            # -------------------------------------------
            else:
                pass  # Unhandled tokens are ignored

        return compiled_code

    def _replace_custom_ops(self, expression):
        """
        Replaces custom operators (slideUp, slideDown, penguinBoost, givePenguins, snowball)
        in the expression string with their equivalent Python operators (+, -, *, /, **).
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
