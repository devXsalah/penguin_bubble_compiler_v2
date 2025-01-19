#Purpose: 
# Tests the functionality of the parser to ensure it correctly validates tokens and handles syntax errors appropriately.

"""
Explanation:

Purpose: Ensures that the Parser correctly validates tokens and raises appropriate errors for syntactic issues.
Test Cases:
Valid Tokens: Tests various valid token types to ensure they pass parsing without errors.
Invalid Tokens: Tests scenarios where required fields are missing, expecting SyntaxError to be raised.
Edge Cases: Includes tests for unrecognized tokens and empty token lists.
"""

import unittest
from compiler.parser import Parser
from compiler.tokens import TokenType

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parse_valid_penguin_say(self):
        tokens = [{"type": TokenType.PENGUIN_SAY, "value": '"Hello, World!"'}]
        parsed = self.parser.parse(tokens)
        self.assertEqual(parsed, tokens)

    def test_parse_valid_penguin_take(self):
        tokens = [{"type": TokenType.PENGUIN_TAKE, "name": "name", "prompt": '"Enter your name:"'}]
        parsed = self.parser.parse(tokens)
        self.assertEqual(parsed, tokens)

    def test_parse_valid_variable_assignment(self):
        tokens = [{"type": TokenType.VARIABLE_ASSIGNMENT, "name": "x", "value": "10"}]
        parsed = self.parser.parse(tokens)
        self.assertEqual(parsed, tokens)

    def test_parse_valid_penguin_do(self):
        tokens = [{
            "type": TokenType.PENGUIN_DO,
            "name": "add",
            "params": "a, b",
            "block": [
                {"type": TokenType.PENGUIN_SAY, "value": '"Adding numbers"'},
                {"type": TokenType.VARIABLE_ASSIGNMENT, "name": "result", "value": "a + b"},
                {"type": TokenType.RETURN_ICE, "value": "result"}
            ]
        }]
        parsed = self.parser.parse(tokens)
        self.assertEqual(parsed, tokens)

    def test_parse_valid_keep_walking(self):
        tokens = [{
            "type": TokenType.KEEP_WALKING,
            "condition": "x < 30",
            "block": [
                {"type": TokenType.PENGUIN_SAY, "value": '"Age is less than 30."'},
                {"type": TokenType.VARIABLE_ASSIGNMENT, "name": "x", "value": "x + 1"}
            ]
        }]
        parsed = self.parser.parse(tokens)
        self.assertEqual(parsed, tokens)

    def test_parse_valid_penguin_if_else(self):
        tokens = [
            {
                "type": TokenType.PENGUIN_IF,
                "condition": "x == z",
                "block": [
                    {"type": TokenType.PENGUIN_SAY, "value": '"x equals z"'}
                ]
            },
            {
                "type": TokenType.PENGUIN_ELSE,
                "block": [
                    {"type": TokenType.PENGUIN_SAY, "value": '"x does not equal z"'}
                ]
            }
        ]
        parsed = self.parser.parse(tokens)
        self.assertEqual(parsed, tokens)

    def test_parse_missing_value_in_penguin_say(self):
        tokens = [{"type": TokenType.PENGUIN_SAY}]
        with self.assertRaises(SyntaxError) as context:
            self.parser.parse(tokens)
        self.assertIn("Missing value in penguinSay statement.", str(context.exception))

    def test_parse_missing_name_in_penguin_take(self):
        tokens = [{"type": TokenType.PENGUIN_TAKE, "prompt": '"Enter your name:"'}]
        with self.assertRaises(SyntaxError) as context:
            self.parser.parse(tokens)
        self.assertIn("Missing name or prompt in penguinTake statement.", str(context.exception))

    def test_parse_missing_prompt_in_penguin_take(self):
        tokens = [{"type": TokenType.PENGUIN_TAKE, "name": "name"}]
        with self.assertRaises(SyntaxError) as context:
            self.parser.parse(tokens)
        self.assertIn("Missing name or prompt in penguinTake statement.", str(context.exception))

    def test_parse_incomplete_variable_assignment(self):
        tokens = [{"type": TokenType.VARIABLE_ASSIGNMENT, "name": "x"}]
        with self.assertRaises(SyntaxError) as context:
            self.parser.parse(tokens)
        self.assertIn("Incomplete variable assignment.", str(context.exception))

    def test_parse_incomplete_penguin_do(self):
        tokens = [{
            "type": TokenType.PENGUIN_DO,
            "name": "add",
            "params": "a, b"
            # Missing "block"
        }]
        with self.assertRaises(SyntaxError) as context:
            self.parser.parse(tokens)
        self.assertIn("Incomplete function definition.", str(context.exception))

    def test_parse_missing_condition_in_keep_walking(self):
        tokens = [{
            "type": TokenType.KEEP_WALKING,
            "block": [
                {"type": TokenType.PENGUIN_SAY, "value": '"Age is less than 30."'}
            ]
        }]
        with self.assertRaises(SyntaxError) as context:
            self.parser.parse(tokens)
        self.assertIn("Missing condition or block in keepWalking statement.", str(context.exception))

    def test_parse_missing_block_in_penguin_if(self):
        tokens = [{
            "type": TokenType.PENGUIN_IF,
            "condition": "x == z"
            # Missing "block"
        }]
        with self.assertRaises(SyntaxError) as context:
            self.parser.parse(tokens)
        self.assertIn("Missing condition or block in penguinIf statement.", str(context.exception))

    def test_parse_missing_block_in_penguin_else(self):
        tokens = [{
            "type": TokenType.PENGUIN_ELSE
            # Missing "block"
        }]
        with self.assertRaises(SyntaxError) as context:
            self.parser.parse(tokens)
        self.assertIn("Missing block in penguinElse statement.", str(context.exception))

    def test_parse_missing_value_in_return_ice(self):
        tokens = [{"type": TokenType.RETURN_ICE}]
        with self.assertRaises(SyntaxError) as context:
            self.parser.parse(tokens)
        self.assertIn("Missing value in returnIce statement.", str(context.exception))

    def test_parse_ignore_unrecognized_tokens(self):
        tokens = [
            {"type": "unknownToken", "value": "some_value"},
            {"type": "penguinSay", "value": '"Hello!"'}
        ]
        # Assuming the parser does not raise errors for unknown tokens
        parsed = self.parser.parse(tokens)
        self.assertEqual(parsed, tokens)  # In current implementation, parser skips unknown tokens

    def test_parse_empty_tokens(self):
        tokens = []
        parsed = self.parser.parse(tokens)
        self.assertEqual(parsed, tokens)

if __name__ == '__main__':
    unittest.main()
