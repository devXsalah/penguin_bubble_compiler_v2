# compiler/tokenizer.py

"""
tokenizer.py

Purpose:
Implements the tokenizer (lexer), responsible for converting raw .pg
source code into a structured list of tokens based on defined token types.

Key Points:
- No external libraries are used (like re).
- For indentation, we use unindent_line from utils.py.
- Arithmetic operations produce operator-specific tokens:
  slideUp -> SLIDE_UP,
  slideDown -> SLIDE_DOWN,
  penguinBoost -> PENGUIN_BOOST,
  givePenguins -> GIVE_PENGUINS,
  snowball -> SNOWBALL
"""

from compiler.tokens import TokenType
from compiler.utils import unindent_line

class Tokenizer:
    def __init__(self):
        pass  # No initialization needed for now

    def tokenize(self, code):
        tokens = []
        lines = code.split("\n")
        i = 0

        while i < len(lines):
            line = lines[i].rstrip()
            if not line.strip():
                i += 1
                continue

            stripped_line = line.strip()
            upper_line = stripped_line.upper()

            # -------------------------------------------------------
            # 1) penguinSay: e.g. penguinSay "Hello World"
            # -------------------------------------------------------
            if upper_line.startswith("PENGUINSAY"):
                # Grab everything after 'penguinSay'
                # e.g. penguinSay "Hello World!"
                value = stripped_line[len("penguinSay"):].strip()
                tokens.append({
                    "type": TokenType.PENGUIN_SAY,
                    "value": value
                })
                i += 1

            # -------------------------------------------------------
            # 2) penguinTake: e.g. penguinTake(num1) "Enter value: "
            # -------------------------------------------------------
            elif upper_line.startswith("PENGUINTAKE"):
                # Syntax: penguinTake(name) "prompt text"
                paren_open = stripped_line.find("(")
                paren_close = stripped_line.find(")")

                if paren_open == -1 or paren_close == -1 or paren_close < paren_open:
                    # Invalid syntax -> skip
                    i += 1
                    continue

                name = stripped_line[paren_open + 1 : paren_close].strip()

                # Extract prompt in quotes (if present)
                prompt = ""
                quote_start = stripped_line.find('"', paren_close)
                if quote_start != -1:
                    quote_end = stripped_line.rfind('"')
                    if quote_end > quote_start:
                        prompt = stripped_line[quote_start : quote_end + 1]
                    else:
                        prompt = ""
                else:
                    # If no quotes, everything after parenthesis is the prompt
                    remainder = stripped_line[paren_close + 1:].strip()
                    prompt = remainder if remainder else ""

                tokens.append({
                    "type": TokenType.PENGUIN_TAKE,
                    "name": name,
                    "prompt": prompt
                })
                i += 1

            # -------------------------------------------------------
            # 3) penguinDo: e.g. penguinDo(addOperation)(x, y)
            # -------------------------------------------------------
            elif upper_line.startswith("PENGUINDO"):
                header = stripped_line[len("penguinDo"):].strip()

                # Extract function name and params
                name, params = self._extract_function_def(header)

                # Gather indented block
                block_lines = []
                i += 1
                while i < len(lines):
                    next_line = lines[i]
                    if next_line.startswith("    ") or next_line.startswith("\t"):
                        block_lines.append(unindent_line(next_line))
                        i += 1
                    else:
                        break

                block_str = "\n".join(block_lines)
                block_tokens = self.tokenize(block_str)

                tokens.append({
                    "type": TokenType.PENGUIN_DO,
                    "name": name,
                    "params": params,
                    "block": block_tokens
                })

            # -------------------------------------------------------
            # 4) keepWalking: e.g. keepWalking(condition)
            # -------------------------------------------------------
            elif upper_line.startswith("KEEP_WALKING"):
                # Everything after 'keepWalking' is the condition
                condition = stripped_line[len("keepWalking"):].strip()

                # Gather indented block
                block_lines = []
                i += 1
                while i < len(lines):
                    next_line = lines[i]
                    if next_line.startswith("    ") or next_line.startswith("\t"):
                        block_lines.append(unindent_line(next_line))
                        i += 1
                    else:
                        break

                # Recursively tokenize the block
                block_tokens = self.tokenize("\n".join(block_lines))
                tokens.append({
                    "type": TokenType.KEEP_WALKING,
                    "condition": condition,
                    "block": block_tokens
                })

            # -------------------------------------------------------
            # 5) penguinIf: e.g. penguinIf(condition)
            # -------------------------------------------------------
            elif upper_line.startswith("PENGUIN_IF"):
                condition = stripped_line[len("penguinIf"):].strip()

                # Gather indented block
                block_lines = []
                i += 1
                while i < len(lines):
                    next_line = lines[i]
                    if next_line.startswith("    ") or next_line.startswith("\t"):
                        block_lines.append(unindent_line(next_line))
                        i += 1
                    else:
                        break

                block_tokens = self.tokenize("\n".join(block_lines))
                tokens.append({
                    "type": TokenType.PENGUIN_IF,
                    "condition": condition,
                    "block": block_tokens
                })

            # -------------------------------------------------------
            # 6) penguinWhatAbout: e.g. penguinWhatAbout(condition)
            #    (analogous to elif)
            # -------------------------------------------------------
            elif (upper_line.startswith("PENGUIN_WHATABOUT") or
                  upper_line.startswith("PENGUIN_WHAT_ABOUT")):

                # Distinguish either 'WHATABOUT' or 'WHAT_ABOUT'
                cmd_len = 0
                if "WHATABOUT" in upper_line:
                    cmd_len = len("PENGUIN_WHATABOUT")
                else:
                    cmd_len = len("PENGUIN_WHAT_ABOUT")

                condition = stripped_line[cmd_len:].strip()

                # Gather indented block
                block_lines = []
                i += 1
                while i < len(lines):
                    next_line = lines[i]
                    if next_line.startswith("    ") or next_line.startswith("\t"):
                        block_lines.append(unindent_line(next_line))
                        i += 1
                    else:
                        break

                block_tokens = self.tokenize("\n".join(block_lines))
                tokens.append({
                    "type": TokenType.PENGUIN_WHAT_ABOUT,
                    "condition": condition,
                    "block": block_tokens
                })

            # -------------------------------------------------------
            # 7) penguinElse: e.g. penguinElse
            # -------------------------------------------------------
            elif upper_line.startswith("PENGUIN_ELSE"):
                # Gather indented block
                block_lines = []
                i += 1
                while i < len(lines):
                    next_line = lines[i]
                    if next_line.startswith("    ") or next_line.startswith("\t"):
                        block_lines.append(unindent_line(next_line))
                        i += 1
                    else:
                        break

                block_tokens = self.tokenize("\n".join(block_lines))
                tokens.append({
                    "type": TokenType.PENGUIN_ELSE,
                    "block": block_tokens
                })

            # -------------------------------------------------------
            # 8) returnIce: e.g. returnIce value
            # -------------------------------------------------------
            elif upper_line.startswith("RETURNICE"):
                value = stripped_line[len("returnIce"):].strip()
                tokens.append({
                    "type": TokenType.RETURN_ICE,
                    "value": value
                })
                i += 1

            # -------------------------------------------------------
            # 9) break: e.g. break
            # -------------------------------------------------------
            elif stripped_line == "break":
                tokens.append({
                    "type": TokenType.PENGUIN_BREAK
                })
                i += 1

            # -------------------------------------------------------
            # 10) Custom arithmetic lines:
            #     slideUp(result) = num1 slideUp num2
            #     slideDown(result) = x slideDown y
            #     etc.
            # -------------------------------------------------------
            elif (upper_line.startswith("SLIDEUP(") or
                  upper_line.startswith("SLIDEDOWN(") or
                  upper_line.startswith("PENGUINBOOST(") or
                  upper_line.startswith("GIVEPENGUINS(") or
                  upper_line.startswith("SNOWBALL(")):

                if upper_line.startswith("SLIDEUP("):
                    op_type = TokenType.SLIDE_UP
                elif upper_line.startswith("SLIDEDOWN("):
                    op_type = TokenType.SLIDE_DOWN
                elif upper_line.startswith("PENGUINBOOST("):
                    op_type = TokenType.PENGUIN_BOOST
                elif upper_line.startswith("GIVEPENGUINS("):
                    op_type = TokenType.GIVE_PENGUINS
                else:  # SNOWBALL(
                    op_type = TokenType.SNOWBALL

                # Extract target name inside parentheses
                paren_open = stripped_line.find("(")
                paren_close = stripped_line.find(")")
                if paren_open == -1 or paren_close == -1 or paren_close < paren_open:
                    i += 1
                    continue

                target_var = stripped_line[paren_open + 1 : paren_close].strip()

                # Find '=' to split out the expression
                eq_index = stripped_line.find("=")
                if eq_index == -1:
                    i += 1
                    continue

                expression = stripped_line[eq_index + 1:].strip()
                tokens.append({
                    "type": op_type,
                    "target": target_var,
                    "expression": expression
                })
                i += 1

            else:
                # Unrecognized or leftover line -> skip
                i += 1

        return tokens

    # -------------------------------------------------------------------
    # Helper function to extract function name and parameters
    # from a string like "addOperation)(x, y)"
    # -------------------------------------------------------------------
    def _extract_function_def(self, header_str):
        name = ""
        params = ""

        # Handle multiple parentheses, e.g., "addOperation)(x, y)"
        first_paren_open = header_str.find('(')
        first_paren_close = header_str.find(')', first_paren_open)

        if first_paren_open != -1 and first_paren_close != -1:
            # Extract function name
            name = header_str[first_paren_open + 1 : first_paren_close].strip()

            # Look for second set of parentheses for parameters
            second_paren_open = header_str.find('(', first_paren_close)
            second_paren_close = header_str.find(')', second_paren_open)

            if second_paren_open != -1 and second_paren_close != -1:
                params = header_str[second_paren_open + 1 : second_paren_close].strip()
        else:
            # Alternative syntax: "addOperation, x, y"
            parts = [x.strip() for x in header_str.split(',')]
            if len(parts) > 0:
                name = parts[0]
                if len(parts) > 1:
                    params = ", ".join(parts[1:])

        return name, params
