"""
main.py

Purpose:
Serves as the compiler's entry point. It processes command-line arguments,
reads the .pg source file, invokes the compiler, and writes the generated
Python code to an output file.

Explanation:
- Argument Parsing (using argparse):
  - source_file: Path to the .pg file to compile.
  - -o / --output: Optional argument to specify the output .py file.
    Defaults to the same basename as the input but with a .py extension.
- File Validation:
  - Checks if the file exists and ends with '.pg'.
- Compilation Process:
  - Reads the source code, initializes the PenguinBubbleCompiler,
    and obtains the compiled Python code as a string.
- Output:
  - Writes the compiled Python code to the specified output file.
  - Prints a success or error message.
"""

import argparse
import os
from compiler.compiler import PenguinBubbleCompiler

def main():
    parser = argparse.ArgumentParser(
        description="PenguinBubbleCompiler: Compile .pg files into Python code."
    )
    parser.add_argument(
        'source_file',
        help='Path to the .pg source file.'
    )
    parser.add_argument(
        '-o', '--output',
        help='Path to the output Python file. Defaults to <source_file>.py',
        default=None
    )

    args = parser.parse_args()

    source_file = args.source_file
    output_file = args.output

    # 1) Validate the source file exists
    if not os.path.isfile(source_file):
        print(f"Error: The source file '{source_file}' does not exist.")
        return

    # 2) Validate the extension is .pg
    if not source_file.endswith('.pg'):
        print("Error: The source file must have a '.pg' extension.")
        return

    # 3) If no output file is specified, use the source filename with .py extension
    if output_file is None:
        output_file = os.path.splitext(source_file)[0] + '.py'

    # 4) Read the .pg source code
    with open(source_file, 'r', encoding='utf-8') as f:
        code = f.read()

    # 5) Compile the source code
    compiler = PenguinBubbleCompiler()
    compiled_code = compiler.compile(code)

    # 6) Write the compiled Python code to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(compiled_code)

    print(f"Compilation successful! Output written to '{output_file}'.")

if __name__ == "__main__":
    main()
