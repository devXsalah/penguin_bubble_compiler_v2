# compiler/parser.py

from compiler.tokens import TokenType

class Parser:
    def __init__(self):
        pass  # No initialization needed for now

    def parse(self, tokens):
        """
        Parses the list of tokens and validates the syntax.
        Optionally, constructs an Abstract Syntax Tree (AST).

        :param tokens: List of tokens to parse.
        :return: Parsed tokens or AST.
        """
        for token in tokens:
            token_type = token["type"]

            if token_type == TokenType.PENGUIN_SAY:
                if "value" not in token:
                    raise SyntaxError("Missing 'value' in penguinSay statement.")

            elif token_type == TokenType.PENGUIN_TAKE:
                if "name" not in token or "prompt" not in token:
                    raise SyntaxError("Missing 'name' or 'prompt' in penguinTake statement.")

            elif token_type == TokenType.PENGUIN_DO:
                if "name" not in token or "params" not in token :
                    raise SyntaxError("Incomplete function definition (penguinDo).")

            elif token_type in [TokenType.KEEP_WALKING, TokenType.PENGUIN_IF, TokenType.PENGUIN_WHAT_ABOUT]:
                if "condition" not in token:
                    raise SyntaxError(f"Missing 'condition' or 'block' in {token_type} statement.")

            elif token_type == TokenType.PENGUIN_ELSE:
                if False:
                    raise SyntaxError("Missing 'block' in penguinElse statement.")

            elif token_type == TokenType.RETURN_ICE:
                if "value" not in token:
                    raise SyntaxError("Missing 'value' in returnIce statement.")
            elif token_type == TokenType.ICE_BUCKET:
                if "value" not in token:
                    raise SyntaxError("Missing 'value' in iceBucket statement.")

            elif token_type in [
                TokenType.SLIDE_UP, 
                TokenType.SLIDE_DOWN, 
                TokenType.PENGUIN_BOOST, 
                TokenType.GIVE_PENGUINS, 
                TokenType.SNOWBALL
            ]:
                if "target" not in token or "expression" not in token:
                    raise SyntaxError("Missing 'target' or 'expression' in arithmetic operation.")

            elif token_type == TokenType.PENGUIN_BREAK:
                # No additional fields required for 'break'
                pass

            else:
                # Handle other token types or ignore
                pass

            # Recursively parse any nested blocks
            if "block" in token:
                block_tokens = token.get("block", [])
                self.parse(block_tokens)

        return tokens  # In this simple parser, we return tokens as-is
