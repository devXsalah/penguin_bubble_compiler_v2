# compiler/tokenizer.py

"""
tokenizer.py

Purpose:
Implements the tokenizer (lexer), responsible for converting raw .pg
source code into a structured list of tokens based on defined token types.

Key Points:
- No external libraries are used (like re).
- Arithmetic operations produce operator-specific tokens:
  slideUp -> SLIDE_UP,
  slideDown -> SLIDE_DOWN,
  penguinBoost -> PENGUIN_BOOST,
  givePenguins -> GIVE_PENGUINS,
  snowball -> SNOWBALL
"""

from compiler.tokens import TokenType

class Tokenizer:
    def __init__(self):
        pass  # No initialization needed for now


    def tokenize(self, code):
        tokens = []
        lines = code.split("\n")
        index = 0

        for ln in lines:
            line = ln.rstrip()
            current_ident = len(line) - len(line.strip())
            
            if not line.strip():
                continue
            
            index += 1
            

            stripped_line = line.strip()
            upper_line = stripped_line.upper()
            # print("LINE: ", upper_line)

            # -------------------------------------------------------
            # 1) penguinSay: e.g. penguinSay "Hello World"
            # -------------------------------------------------------
            if upper_line.startswith("PENGUINSAY"):
                # Grab everything after 'penguinSay'
                # e.g. penguinSay "Hello World!"
                value = stripped_line[len("penguinSay"):].strip()
                tokens.append({
                    "type": TokenType.PENGUIN_SAY,
                    "value": value,
                    "indent": current_ident,
                    "index" : index
                    
                })

            # -------------------------------------------------------
            # 2) penguinTake: e.g. penguinTake(num1) "Enter value: "
            # -------------------------------------------------------
            elif upper_line.startswith("PENGUINTAKE"):
                # Syntax: penguinTake(name) "prompt text"
                paren_open = stripped_line.find("(")
                paren_close = stripped_line.find(")")

                if paren_open == -1 or paren_close == -1 or paren_close < paren_open:

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
                    "prompt": prompt,
                    "indent": current_ident,
                    "index" : index
                })
                
            # -------------------------------------------------------
            # 8) returnIce: e.g. returnIce value
            # -------------------------------------------------------
                
            elif upper_line.startswith("RETURNICE"):
                # Everything after 'keepWalking' is the condition
                value = stripped_line[len("returnIce"):].strip()

                tokens.append({
                    "type": TokenType.RETURN_ICE,
                    "value": value,
                    "indent": current_ident,
                    "index" : index
                })
                


            # -------------------------------------------------------
            # 3) penguinDo: e.g. penguinDo(addOperation)(x, y)
            # -------------------------------------------------------
            elif upper_line.startswith("PENGUINDO"):
                header = stripped_line[len("penguinDo"):].strip()

                # Extract function name and params
                name, params = self._extract_function_def(header)

                tokens.append({
                    "type": TokenType.PENGUIN_DO,
                    "name": name,
                    "params": params,
                    "indent": current_ident,
                    "index" : index
                })

            # -------------------------------------------------------
            # 4) keepWalking: e.g. keepWalking(condition)
            # -------------------------------------------------------
            elif upper_line.startswith("KEEPWALKING"):
                # Everything after 'keepWalking' is the condition
                condition = stripped_line[len("keepWalking"):].strip()

                

                tokens.append({
                    "type": TokenType.KEEP_WALKING,
                    "condition": condition,
                    "indent": current_ident,
                    "index" : index
                })

            # -------------------------------------------------------
            # 5) penguinIf: e.g. penguinIf(condition)
            # -------------------------------------------------------
            elif upper_line.startswith("PENGUINIF"):
                condition = stripped_line[len("penguinIf"):].strip()


                

                tokens.append({
                    "type": TokenType.PENGUIN_IF,
                    "condition": condition,
                    "indent": current_ident,
                    "index" : index
                })

            # -------------------------------------------------------
            # 6) penguinWhatAbout: e.g. penguinWhatAbout(condition)
            #    (analogous to elif)
            # -------------------------------------------------------
            elif upper_line.startswith("PENGUINWHATABOUT"):

                # Distinguish either 'WHATABOUT' or 'WHAT_ABOUT'
                cmd_len = 0
                if "WHATABOUT" in upper_line:
                    cmd_len = len("PENGUINWHATABOUT")
                else:
                    cmd_len = len("PENGUIN_WHAT_ABOUT")

                condition = stripped_line[cmd_len:].strip()


                
                tokens.append({
                    "type": TokenType.PENGUIN_WHAT_ABOUT,
                    "condition": condition,
                    "indent": current_ident,
                    "index" : index
                })

            # -------------------------------------------------------
            # 7) penguinElse: e.g. penguinElse
            # -------------------------------------------------------
            elif upper_line.startswith("PENGUINELSE"):
                # Gather indented block

                
                tokens.append({
                    "type": TokenType.PENGUIN_ELSE,
                    "indent": current_ident,
                    "index" : index
                })

            # # -------------------------------------------------------
            # # 8) returnIce: e.g. returnIce value
            # # -------------------------------------------------------
                
            # elif upper_line.startswith("RETURNICE"):
            #     # Everything after 'keepWalking' is the condition
            #     value = stripped_line[len("returnIce"):].strip()

            #     tokens.append({
            #         "type": TokenType.RETURN_ICE,
            #         "value": value,
            #         "indent": current_ident
            #     })
                
            # -------------------------------------------------------
            # 8) iceBucket:
            # -------------------------------------------------------
            elif upper_line.startswith("ICEBUCKET"):
                value = stripped_line[len("iceBucket"):].strip()
                
                tokens.append({
                    "type": TokenType.ICE_BUCKET,
                    "value": value,
                    "indent": current_ident,
                    "index" : index
                })

            # -------------------------------------------------------
            # 9) break: e.g. break
            # -------------------------------------------------------
            elif stripped_line == "break":
                tokens.append({
                    "type": TokenType.PENGUIN_BREAK,
                    "indent": current_ident,
                    "index" : index
                })

            # print(tokens[-1])
        # print(tokens)

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
