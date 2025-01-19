#Purpose: Serves as the compiler's entry point. 
# It processes command-line arguments, 
# reads the .pg source file, 
# invokes the compiler, 
# and writes the generated Python code to an output file.

# main.py
import argparse
import os
from compiler.compiler import PenguinBubbleCompiler

def main():
    parser = argparse.ArgumentParser(description="PenguinBubbleCompiler: Compile .pg files to Python code.")
    parser.add_argument('source_file', help='Path to the .pg source file')
    parser.add_argument('-o', '--output', help='Path to the output Python file', default=None)
    
    args = parser.parse_args()
    
    source_file = args.source_file
    output_file = args.output
    
    # Validate source file existence
    if not os.path.isfile(source_file):
        print(f"Error: The source file '{source_file}' does not exist.")
        return
    
    # Validate source file extension
    if not source_file.endswith('.pg'):
        print("Error: The source file must have a '.pg' extension.")
        return
    
    # Set default output file if not provided
    if output_file is None:
        output_file = os.path.splitext(source_file)[0] + '.py'
    
    # Read the source code from the .pg file
    with open(source_file, 'r') as f:
        code = f.read()
    
    # Initialize and run the compiler
    compiler = PenguinBubbleCompiler()
    compiled_code = compiler.compile(code)
    
    # Write the compiled Python code to the output file
    with open(output_file, 'w') as f:
        f.write(compiled_code)
    
    print(f"Compilation successful! Output written to '{output_file}'.")

if __name__ == "__main__":
    main()
