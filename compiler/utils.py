#Purpose: 
# Contains utility functions that support various parts of the compiler, 
# such as indentation handling and error formatting.

"""
Explanation:

indent_code Function:
Purpose: Adds indentation to each line of a given code block.
Parameters:
code: The code string to indent.
level: The number of indentation levels (default is 1).
indent_str: The string used for indentation (default is 4 spaces).
Usage: Ensures that blocks like function bodies, loops, and conditionals are properly indented in the generated Python code.
"""

def indent_code(code, level=1, indent_str="    "):
    """
    Indents each line of the provided code by the specified level.
    
    :param code: The code string to indent.
    :param level: The indentation level.
    :param indent_str: The string used for indentation (default is 4 spaces).
    :return: The indented code string.
    """
    indentation = indent_str * level
    return '\n'.join([indentation + line if line else line for line in code.split('\n')])
