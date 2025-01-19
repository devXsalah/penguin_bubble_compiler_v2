#Purpose: 
# Implements the parser, 
# responsible for syntax validation and potentially building an Abstract Syntax Tree (AST).
#  In this implementation, 
# the parser ensures that the tokens adhere to the language's syntax rules

"""
Explanation:

parse Method:
Purpose: Validates the syntax of the token list.
Functionality:
Iterates through each token and checks for the presence of required fields based on the token type.
Raises SyntaxError if any required field is missing.
Extensibility: Can be expanded to build an Abstract Syntax Tree (AST) or perform more complex syntax analyses in the future.
"""

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
        # For simplicity, we'll perform basic syntax validation here.
        # Advanced implementations can build an AST.
        for token in tokens:
            token_type = token["type"]
            if token_type == TokenType.PENGUIN_SAY:
                if "value" not in token:
                    raise SyntaxError("Missing value in penguinSay statement.")
            elif token_type == TokenType.PENGUIN_TAKE:
                if "name" not in token or "prompt" not in token:
                    raise SyntaxError("Missing name or prompt in penguinTake statement.")
            elif token_type == TokenType.VARIABLE_ASSIGNMENT:
                if "name" not in token or "value" not in token:
                    raise SyntaxError("Incomplete variable assignment.")
            elif token_type == TokenType.PENGUIN_DO:
                if "name" not in token or "params" not in token or "block" not in token:
                    raise SyntaxError("Incomplete function definition.")
                # Further validation can be added here
            elif token_type in [TokenType.KEEP_WALKING, TokenType.PENGUIN_IF, TokenType.PENGUIN_WHAT_ABOUT]:
                if "condition" not in token or "block" not in token:
                    raise SyntaxError(f"Missing condition or block in {token_type} statement.")
            elif token_type == TokenType.PENGUIN_ELSE:
                if "block" not in token:
                    raise SyntaxError("Missing block in penguinElse statement.")
            elif token_type == TokenType.RETURN_ICE:
                if "value" not in token:
                    raise SyntaxError("Missing value in returnIce statement.")
            else:
                # Handle other token types or ignore
                pass
        return tokens  # In this simple parser, we return tokens as-is
