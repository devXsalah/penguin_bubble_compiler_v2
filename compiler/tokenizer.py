"""
Purpose:
Implements the tokenizer (lexer), responsible for converting raw .pg
source code into a structured list of tokens based on defined token types.

Key Points:
- No external libraries are used (like re).
- The tokenizer identifies specific commands and translates them into tokenized
  representations with associated metadata like indentation level and line number.
"""

from compiler.tokens import TokenType

class Tokenizer:
    def __init__(self):
        pass  # No initialization needed for now

    def tokenize(self, code):
        """
        Converts the input code string into a list of tokens. Each token is represented
        as a dictionary containing the type, value, indentation level, and line index.
        """
        tokens = []
        lines = code.split("\n")
        index = 0

        for ln in lines:
            line = ln.rstrip()
            current_ident = len(line) - len(line.strip())  # Determine indentation level
            
            if not line.strip():
                continue  # Skip empty lines
            
            index += 1  # Track line numbers for debugging and metadata
            stripped_line = line.strip()
            upper_line = stripped_line.upper()

            # -------------------------------------------------------
            # Tokenize penguinSay command
            # Example: penguinSay "Hello World"
            # -------------------------------------------------------
            if upper_line.startswith("PENGUINSAY"):
                value = stripped_line[len("penguinSay"):].strip()
                tokens.append({
                    "type": TokenType.PENGUIN_SAY,
                    "value": value,
                    "indent": current_ident,
                    "index": index
                })

            # -------------------------------------------------------
            # Tokenize penguinTake command
            # Example: penguinTake(variableName) "prompt text"
            # -------------------------------------------------------
            elif upper_line.startswith("PENGUINTAKE"):
                paren_open = stripped_line.find("(")
                paren_close = stripped_line.find(")")
                
                # Validate parentheses
                if paren_open == -1 or paren_close == -1 or paren_close < paren_open:
                    continue

                name = stripped_line[paren_open + 1:paren_close].strip()

                # Extract optional prompt text in quotes
                quote_start = stripped_line.find('"', paren_close)
                if quote_start != -1:
                    quote_end = stripped_line.rfind('"')
                    prompt = stripped_line[quote_start:quote_end + 1] if quote_end > quote_start else ""
                else:
                    prompt = stripped_line[paren_close + 1:].strip()

                tokens.append({
                    "type": TokenType.PENGUIN_TAKE,
                    "name": name,
                    "prompt": prompt,
                    "indent": current_ident,
                    "index": index
                })

            # -------------------------------------------------------
            # Tokenize returnIce command
            # Example: returnIce value
            # -------------------------------------------------------
            elif upper_line.startswith("RETURNICE"):
                value = stripped_line[len("returnIce"):].strip()
                tokens.append({
                    "type": TokenType.RETURN_ICE,
                    "value": value,
                    "indent": current_ident,
                    "index": index
                })

            # -------------------------------------------------------
            # Tokenize breakIce command
            # Example: breakIce
            # -------------------------------------------------------
            elif upper_line.startswith("BREAKICE"):
                tokens.append({
                    "type": TokenType.BREAKICE,
                    "value": "",  # No value expected for breakIce
                    "indent": current_ident,
                    "index": index
                })

            # -------------------------------------------------------
            # Tokenize penguinDo command
            # Example: penguinDo(addOperation)(x, y)
            # -------------------------------------------------------
            elif upper_line.startswith("PENGUINDO"):
                header = stripped_line[len("penguinDo"):].strip()
                name, params = self._extract_function_def(header)

                tokens.append({
                    "type": TokenType.PENGUIN_DO,
                    "name": name,
                    "params": params,
                    "indent": current_ident,
                    "index": index
                })

            # -------------------------------------------------------
            # Tokenize keepWalking command
            # Example: keepWalking(condition)
            # -------------------------------------------------------
            elif upper_line.startswith("KEEPWALKING"):
                condition = stripped_line[len("keepWalking"):].strip()
                tokens.append({
                    "type": TokenType.KEEP_WALKING,
                    "condition": condition,
                    "indent": current_ident,
                    "index": index
                })

            # -------------------------------------------------------
            # Tokenize penguinIf command
            # Example: penguinIf(condition)
            # -------------------------------------------------------
            elif upper_line.startswith("PENGUINIF"):
                condition = stripped_line[len("penguinIf"):].strip()
                tokens.append({
                    "type": TokenType.PENGUIN_IF,
                    "condition": condition,
                    "indent": current_ident,
                    "index": index
                })

            # -------------------------------------------------------
            # Tokenize penguinWhatAbout command
            # Example: penguinWhatAbout(condition) (similar to elif)
            # -------------------------------------------------------
            elif upper_line.startswith("PENGUINWHATABOUT"):
                cmd_len = len("PENGUINWHATABOUT")
                condition = stripped_line[cmd_len:].strip()
                tokens.append({
                    "type": TokenType.PENGUIN_WHAT_ABOUT,
                    "condition": condition,
                    "indent": current_ident,
                    "index": index
                })

            # -------------------------------------------------------
            # Tokenize penguinElse command
            # Example: penguinElse
            # -------------------------------------------------------
            elif upper_line.startswith("PENGUINELSE"):
                tokens.append({
                    "type": TokenType.PENGUIN_ELSE,
                    "indent": current_ident,
                    "index": index
                })

            # -------------------------------------------------------
            # Tokenize iceBucket command
            # Example: iceBucket value
            # -------------------------------------------------------
            elif upper_line.startswith("ICEBUCKET"):
                value = stripped_line[len("iceBucket"):].strip()
                tokens.append({
                    "type": TokenType.ICE_BUCKET,
                    "value": value,
                    "indent": current_ident,
                    "index": index
                })

        return tokens

    def _extract_function_def(self, header_str):
        """
        Helper function to extract function name and parameters from a header string.
        Handles cases like "addOperation)(x, y)" or "addOperation, x, y".
        """
        name = ""
        params = ""

        first_paren_open = header_str.find('(')
        first_paren_close = header_str.find(')', first_paren_open)

        if first_paren_open != -1 and first_paren_close != -1:
            name = header_str[first_paren_open + 1:first_paren_close].strip()
            second_paren_open = header_str.find('(', first_paren_close)
            second_paren_close = header_str.find(')', second_paren_open)

            if second_paren_open != -1 and second_paren_close != -1:
                params = header_str[second_paren_open + 1:second_paren_close].strip()
        else:
            parts = [x.strip() for x in header_str.split(',')]
            if parts:
                name = parts[0]
                if len(parts) > 1:
                    params = ", ".join(parts[1:])

        return name, params
