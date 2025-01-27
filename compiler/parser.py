from compiler.tokens import TokenType

class Parser:
    def __init__(self):
        pass  # No initialization needed for now

    def parse(self, tokens):
        """
        Parses the list of tokens and validates their syntax.
        Ensures that required fields are present for each token type.
        Optionally, this can be extended to construct an Abstract Syntax Tree (AST).

        :param tokens: List of tokens to parse.
        :return: Parsed tokens (or AST in an extended implementation).
        """
        for token in tokens:
            token_type = token["type"]

            # -------------------------------------------------------
            # Validate penguinSay token
            # Requires: "value"
            # -------------------------------------------------------
            if token_type == TokenType.PENGUIN_SAY:
                if "value" not in token:
                    raise SyntaxError("Missing 'value' in penguinSay statement.")

            # -------------------------------------------------------
            # Validate penguinTake token
            # Requires: "name", "prompt"
            # -------------------------------------------------------
            elif token_type == TokenType.PENGUIN_TAKE:
                if "name" not in token or "prompt" not in token:
                    raise SyntaxError("Missing 'name' or 'prompt' in penguinTake statement.")

            # -------------------------------------------------------
            # Validate penguinDo token
            # Requires: "name", "params"
            # -------------------------------------------------------
            elif token_type == TokenType.PENGUIN_DO:
                if "name" not in token or "params" not in token:
                    raise SyntaxError("Incomplete function definition (penguinDo).")

            # -------------------------------------------------------
            # Validate condition-based tokens
            # Includes: keepWalking, penguinIf, penguinWhatAbout
            # Requires: "condition"
            # -------------------------------------------------------
            elif token_type in [TokenType.KEEP_WALKING, TokenType.PENGUIN_IF, TokenType.PENGUIN_WHAT_ABOUT]:
                if "condition" not in token:
                    raise SyntaxError(f"Missing 'condition' in {token_type} statement.")

            # -------------------------------------------------------
            # Validate returnIce token
            # Requires: "value"
            # -------------------------------------------------------
            elif token_type == TokenType.RETURN_ICE:
                if "value" not in token:
                    raise SyntaxError("Missing 'value' in returnIce statement.")

            # -------------------------------------------------------
            # Validate iceBucket token
            # Requires: "value"
            # -------------------------------------------------------
            elif token_type == TokenType.ICE_BUCKET:
                if "value" not in token:
                    raise SyntaxError("Missing 'value' in iceBucket statement.")

            # -------------------------------------------------------
            # Validate arithmetic operations
            # Includes: slideUp, slideDown, penguinBoost, givePenguins, snowball
            # Requires: "target", "expression"
            # -------------------------------------------------------
            elif token_type in [
                TokenType.SLIDE_UP,
                TokenType.SLIDE_DOWN,
                TokenType.PENGUIN_BOOST,
                TokenType.GIVE_PENGUINS,
                TokenType.SNOWBALL,
            ]:
                if "target" not in token or "expression" not in token:
                    raise SyntaxError("Missing 'target' or 'expression' in arithmetic operation.")

            # -------------------------------------------------------
            # Validate breakIce token
            # No additional fields required
            # -------------------------------------------------------
            elif token_type == TokenType.BREAKICE:
                pass

            # -------------------------------------------------------
            # Handle other token types or ignore
            # -------------------------------------------------------
            else:
                pass

        # In this simple implementation, tokens are returned as-is.
        return tokens
