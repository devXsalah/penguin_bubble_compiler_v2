#Purpose: 
# Implements the tokenizer (lexer), 
# responsible for converting raw .pg 
# source code into a structured list of tokens based on defined token types.

"""
Explanation:

Token Types Handled:
penguinSay: For printing messages.
penguinTake: For taking user input.
keepWalking: Represents a while loop.
penguinIf, penguinWhatAbout, penguinElse: Represents if, elif, and else statements.
penguinDo: For defining functions.
Variable Assignments: Assigns values to variables.
Arithmetic Operations: Custom operations like slideUp, slideDown, etc., mapped to Python arithmetic operators.
returnIce: For returning values from functions.
Recursive Tokenization: Handles nested blocks by recursively tokenizing indented lines.
Custom Arithmetic Operations: Maps custom commands to standard arithmetic operators.
Error Handling: Skips unrecognized lines silently (can be enhanced for better feedback).
"""

from compiler.tokens import TokenType
from textwrap import dedent

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

            # Match penguinSay
            if stripped_line.upper().startswith("PENGUINSAY"):
                value = stripped_line[len("PENGUINSAY"):].strip()
                tokens.append({"type": TokenType.PENGUIN_SAY, "value": value})
                i += 1

            # Match penguinTake
            elif stripped_line.upper().startswith("PENGUINTAKE"):
                # Assuming syntax: penguinTake(name) "prompt"
                # Extract name
                name_start = stripped_line.find('(') + 1
                name_end = stripped_line.find(')')
                if name_start == 0 or name_end == -1:
                    # Invalid syntax, skip
                    i += 1
                    continue
                name = stripped_line[name_start:name_end].strip()

                # Extract prompt
                prompt_start = stripped_line.find('"')
                if prompt_start != -1:
                    prompt_end = stripped_line.rfind('"')
                    prompt = stripped_line[prompt_start:prompt_end+1]  # Include quotes
                else:
                    # Prompt is an expression
                    # Assuming prompt follows penguinTake(name) without quotes
                    prompt = stripped_line.split(')', 1)[1].strip()
                tokens.append({"type": TokenType.PENGUIN_TAKE, "name": name, "prompt": prompt})
                i += 1

            # Match KEEP_WALKING
            elif stripped_line.upper().startswith("KEEP_WALKING"):
                # Syntax: KEEP_WALKING condition
                condition = stripped_line[len("KEEP_WALKING"):].strip()

                # Collect the block lines
                block_lines = []
                i += 1
                while i < len(lines) and (lines[i].startswith('    ') or lines[i].startswith('\t')):
                    line_content = lines[i][4:] if lines[i].startswith('    ') else lines[i][1:]
                    block_lines.append(line_content)
                    i += 1
                # Tokenize the block recursively
                block_tokens = self.tokenize('\n'.join(block_lines))
                tokens.append({"type": TokenType.KEEP_WALKING, "condition": condition, "block": block_tokens})

            # Match PENGUIN_IF
            elif stripped_line.upper().startswith("PENGUIN_IF"):
                # Syntax: PENGUIN_IF condition
                condition = stripped_line[len("PENGUIN_IF"):].strip()

                # Collect the block lines
                block_lines = []
                i += 1
                while i < len(lines) and (lines[i].startswith('    ') or lines[i].startswith('\t')):
                    line_content = lines[i][4:] if lines[i].startswith('    ') else lines[i][1:]
                    block_lines.append(line_content)
                    i += 1
                # Tokenize the block recursively
                block_tokens = self.tokenize('\n'.join(block_lines))
                tokens.append({"type": TokenType.PENGUIN_IF, "condition": condition, "block": block_tokens})

            # Match PENGUIN_WHAT_ABOUT (elif)
            elif stripped_line.upper().startswith("PENGUIN_WHATABOUT") or stripped_line.upper().startswith("PENGUIN_WHAT_ABOUT"):
                # Handle possible variations in command name
                # Assuming 'PENGUIN_WHATABOUT' or 'PENGUIN_WHAT_ABOUT'

                # Find the exact command string
                if "WHATABOUT" in stripped_line.upper():
                    command_length = len("PENGUIN_WHATABOUT")
                elif "WHAT_ABOUT" in stripped_line.upper():
                    command_length = len("PENGUIN_WHAT_ABOUT")
                else:
                    command_length = len("PENGUIN_WHATABOUT")

                # Syntax: PENGUIN_WHAT_ABOUT condition
                condition = stripped_line[command_length:].strip()

                # Collect the block lines
                block_lines = []
                i += 1
                while i < len(lines) and (lines[i].startswith('    ') or lines[i].startswith('\t')):
                    line_content = lines[i][4:] if lines[i].startswith('    ') else lines[i][1:]
                    block_lines.append(line_content)
                    i += 1
                # Tokenize the block recursively
                block_tokens = self.tokenize('\n'.join(block_lines))
                tokens.append({"type": TokenType.PENGUIN_WHAT_ABOUT, "condition": condition, "block": block_tokens})

            # Match PENGUIN_ELSE
            elif stripped_line.upper().startswith("PENGUIN_ELSE"):
                # Syntax: PENGUIN_ELSE
                # No condition

                # Collect the block lines
                block_lines = []
                i += 1
                while i < len(lines) and (lines[i].startswith('    ') or lines[i].startswith('\t')):
                    line_content = lines[i][4:] if lines[i].startswith('    ') else lines[i][1:]
                    block_lines.append(line_content)
                    i += 1
                # Tokenize the block recursively
                block_tokens = self.tokenize('\n'.join(block_lines))
                tokens.append({"type": TokenType.PENGUIN_ELSE, "block": block_tokens})

            # Match penguinDo
            elif stripped_line.upper().startswith("PENGUINDO"):
                # Assuming syntax: penguinDo(name, params) or penguinDo(name(params))
                # For the test case, not relevant.

                header = stripped_line

                # Collect the block lines
                block_lines = []
                i += 1
                while i < len(lines) and (lines[i].startswith('    ') or lines[i].startswith('\t')):
                    line_content = lines[i][4:] if lines[i].startswith('    ') else lines[i][1:]
                    block_lines.append(line_content)
                    i += 1
                block = '\n'.join(block_lines)

                # Extract name and params
                # Assuming syntax: penguinDo(name, params) or penguinDo(name(params))
                # Need to extract name and params accordingly

                # Check for '('
                name_start = stripped_line.find('(') + 1
                name_end = stripped_line.find(')')
                if name_start > 0 and name_end > name_start:
                    name_params = stripped_line[name_start:name_end].strip()
                    if ',' in name_params:
                        name, params = name_params.split(',', 1)
                        name = name.strip()
                        params = params.strip()
                    else:
                        # Assume params are in another format
                        name = name_params
                        params = ""
                else:
                    # No params
                    name = stripped_line[len("PENGUINDO"):].strip()
                    params = ""

                # Tokenize the block recursively
                block_tokens = self.tokenize(block)
                tokens.append({"type": TokenType.PENGUIN_DO, "name": name, "params": params, "block": block_tokens})

            # Match Variable Assignment
            elif "=" in line and not any(stripped_line.upper().startswith(op.upper()) for op in ["SLIDEUP", "SLIDEDOWN", "PENGUINBOOST", "GIVEPENGUINS", "SNOWBALL"]):
                name, value = line.strip().split("=", 1)
                tokens.append({"type": TokenType.VARIABLE_ASSIGNMENT, "name": name.strip(), "value": value.strip()})
                i += 1

            # Match arithmetic operations
            elif any(stripped_line.upper().startswith(op.upper()) for op in ["SLIDEUP", "SLIDEDOWN", "PENGUINBOOST", "GIVEPENGUINS", "SNOWBALL"]):
                # Handle arithmetic operations as variable assignments
                op_map = {
                    "SLIDEUP": "+",
                    "SLIDEDOWN": "-",
                    "PENGUINBOOST": "*",
                    "GIVEPENGUINS": "/",
                    "SNOWBALL": "**"
                }
                matched_op = None
                for op_key, op_symbol in op_map.items():
                    if stripped_line.upper().startswith(op_key):
                        matched_op = (op_key, op_symbol)
                        break
                if matched_op:
                    op_key, op_symbol = matched_op
                    line_content = stripped_line[len(op_key):].strip()
                    # Assuming syntax like: SLIDEUP(total) = x + y
                    # So, name is within parentheses
                    if '(' in line_content and ')' in line_content:
                        var_start = line_content.find('(') + 1
                        var_end = line_content.find(')')
                        var_name = line_content[var_start:var_end].strip()
                        expr = line_content.split("=", 1)[1].strip()
                        tokens.append({
                            "type": TokenType.VARIABLE_ASSIGNMENT,  # Use the same token type
                            "name": var_name,
                            "value": expr.replace(op_key, op_symbol)  # Replace custom op with symbol
                        })
                    else:
                        # Handle other possible syntaxes
                        if '=' in line_content:
                            var_name, expr = line_content.split("=", 1)
                            tokens.append({
                                "type": TokenType.VARIABLE_ASSIGNMENT,
                                "name": var_name.strip(),
                                "value": expr.strip().replace(op_key, op_symbol)
                            })
                i += 1

            # Match returnIce
            elif stripped_line.upper().startswith("RETURNICE"):
                value = stripped_line[len("RETURNICE"):].strip()
                tokens.append({"type": TokenType.RETURN_ICE, "value": value})
                i += 1

            else:
                # Handle other lines or skip
                i += 1
        return tokens
