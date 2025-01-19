#Purpose: 
# Defines the various token types used by the tokenizer and parser. 
# Using constants ensures consistency across the compiler.

"""
Explanation:

TokenType Class: Contains string constants representing each token type in the PenguinBubble language.
Extensibility: Easily add new token types as the language evolves by extending this class.
"""

class TokenType:
    PENGUIN_SAY = "penguinSay"
    PENGUIN_TAKE = "penguinTake"
    KEEP_WALKING = "keepWalking"
    PENGUIN_IF = "penguinIf"
    PENGUIN_WHAT_ABOUT = "penguinWhatAbout"
    PENGUIN_ELSE = "penguinElse"
    PENGUIN_DO = "penguinDo"
    VARIABLE_ASSIGNMENT = "variableAssignment"
    RETURN_ICE = "returnIce"
