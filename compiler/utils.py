"""
Purpose:
Contains utility functions that support various parts of the compiler,
such as indentation handling and error formatting.
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
    lines = code.split('\n')
    indented_lines = []
    for line in lines:
        # Only indent non-empty lines
        if line.strip():
            indented_lines.append(indentation + line)
        else:
            indented_lines.append(line)
    return '\n'.join(indented_lines)


def unindent_line(line, indent_str="    "):
    """
    Removes one level of indentation (4 spaces or 1 tab) from the given line,
    if present.
    
    :param line: A single line of code to unindent.
    :param indent_str: The string used for indentation (default is 4 spaces).
    :return: The unindented line (if it was indented), otherwise the original line.
    """
    if line.startswith(indent_str):
        # Remove 4 spaces
        return line[len(indent_str):]
    elif line.startswith("\t"):
        # Remove a single tab
        return line[1:]
    else:
        return line
