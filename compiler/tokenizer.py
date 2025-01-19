#Purpose: 
# Implements the tokenization logic, 
# converting raw .pg code into a list of tokens based on defined token types.

# The Tokenizer class provides a tokenize method that processes the raw .pg code line by line,
class Tokenizer:
    def __init__(self):
        pass  # No initialization needed

    def tokenize(self, code):
        tokens = []
        lines = code.split("\n")
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()

            if not line.strip():
                i += 1
                continue

            if line.strip().startswith("penguinSay"):
                value = line.strip()[len("penguinSay"):].strip()
                tokens.append({"type": "penguinSay", "value": value})
                i += 1

            elif line.strip().startswith("penguinTake"):
                name_start = line.find('(') + 1
                name_end = line.find(')')
                params = line[name_start:name_end].split(',')
                name = params[0].strip()

                # Extract prompt without enforcing quotes
                prompt_start = line.find('"')
                if prompt_start != -1:
                    # Prompt is a string literal
                    prompt_end = line.rfind('"')
                    prompt = line[prompt_start:prompt_end+1]  # Include quotes
                else:
                    # Prompt is an expression
                    # Assuming prompt follows penguinTake(name) without quotes
                    prompt = line.strip().split(')', 1)[1].strip()
                tokens.append({"type": "penguinTake", "name": name, "prompt": prompt})
                i += 1

            elif line.strip().startswith("keepWalking"):
                condition_start = line.find('(') + 1
                condition_end = line.find(')')
                condition = line[condition_start:condition_end].strip()

                # Collect the block lines
                block_lines = []
                i += 1
                while i < len(lines) and (lines[i].startswith('    ') or lines[i].startswith('\t')):
                    line_content = lines[i][4:] if lines[i].startswith('    ') else lines[i][1:]
                    block_lines.append(line_content)
                    i += 1
                # Tokenize the block recursively
                block_tokens = self.tokenize('\n'.join(block_lines))
                tokens.append({"type": "keepWalking", "condition": condition, "block": block_tokens})

            elif line.strip().startswith("penguinIf"):
                condition_start = line.find('(') + 1
                condition_end = line.find(')')
                condition = line[condition_start:condition_end].strip()

                # Collect the block lines
                block_lines = []
                i += 1
                while i < len(lines) and (lines[i].startswith('    ') or lines[i].startswith('\t')):
                    line_content = lines[i][4:] if lines[i].startswith('    ') else lines[i][1:]
                    block_lines.append(line_content)
                    i += 1
                # Tokenize the block recursively
                block_tokens = self.tokenize('\n'.join(block_lines))
                tokens.append({"type": "penguinIf", "condition": condition, "block": block_tokens})

            elif line.strip().startswith("penguinWhatAbout"):
                condition_start = line.find('(') + 1
                condition_end = line.find(')')
                condition = line[condition_start:condition_end].strip()

                # Collect the block lines
                block_lines = []
                i += 1
                while i < len(lines) and (lines[i].startswith('    ') or lines[i].startswith('\t')):
                    line_content = lines[i][4:] if lines[i].startswith('    ') else lines[i][1:]
                    block_lines.append(line_content)
                    i += 1
                # Tokenize the block recursively
                block_tokens = self.tokenize('\n'.join(block_lines))
                tokens.append({"type": "penguinWhatAbout", "condition": condition, "block": block_tokens})

            elif line.strip().startswith("penguinElse"):
                # Collect the block lines
                block_lines = []
                i += 1
                while i < len(lines) and (lines[i].startswith('    ') or lines[i].startswith('\t')):
                    line_content = lines[i][4:] if lines[i].startswith('    ') else lines[i][1:]
                    block_lines.append(line_content)
                    i += 1
                # Tokenize the block recursively
                block_tokens = self.tokenize('\n'.join(block_lines))
                tokens.append({"type": "penguinElse", "block": block_tokens})

            elif line.strip().startswith("penguinDo"):
                header = line.strip()

                # Collect the block lines
                block_lines = []
                i += 1
                while i < len(lines) and (lines[i].startswith('    ') or lines[i].startswith('\t')):
                    line_content = lines[i][4:] if lines[i].startswith('    ') else lines[i][1:]
                    block_lines.append(line_content)
                    i += 1
                block = '\n'.join(block_lines)

                name_start = header.find("penguinDo") + len("penguinDo")
                name_end = header.find("(")
                name = header[name_start:name_end].strip()
                params_start = header.find("(") + 1
                params_end = header.find(")")
                params = header[params_start:params_end].strip()
                # Tokenize the block recursively
                block_tokens = self.tokenize(block)
                tokens.append({"type": "penguinDo", "name": name, "params": params, "block": block_tokens})

            elif "=" in line and not any(line.strip().startswith(op) for op in ["slideUp", "slideDown", "penguinBoost", "givePenguins", "snowball"]):
                name, value = line.strip().split("=", 1)
                tokens.append({"type": "variableAssignment", "name": name.strip(), "value": value.strip()})
                i += 1

            elif any(line.strip().startswith(op) for op in ["slideUp", "slideDown", "penguinBoost", "givePenguins", "snowball"]):
                # Handle arithmetic operations as variable assignments
                op_map = {
                    "slideUp": "+",
                    "slideDown": "-",
                    "penguinBoost": "*",
                    "givePenguins": "/",
                    "snowball": "**"
                }
                for op_key, op_symbol in op_map.items():
                    if line.strip().startswith(op_key):
                        line_content = line.strip()[len(op_key):].strip()
                        result, expr = line_content.split("=", 1)
                        tokens.append({
                            "type": "variableAssignment",
                            "name": result.strip(),
                            "value": expr.strip()
                        })
                        break
                i += 1

            elif line.strip().startswith("returnIce"):
                value = line.strip()[len("returnIce"):].strip()
                tokens.append({"type": "returnIce", "value": value})
                i += 1

            else:
                # Handle other lines or skip
                i += 1
        return tokens
