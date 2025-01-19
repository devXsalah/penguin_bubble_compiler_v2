# PenguinBubbleCompiler

**PenguinBubbleCompiler** is a custom compiler designed to translate `.pg` (PenguinBubble) source files into executable Python code. This compiler is built from scratch without relying on external tokenizer or parser libraries, ensuring a deep understanding of the compilation process and facilitating future enhancements.

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Features](#2-features)
3. [Directory Structure](#3-directory-structure)
4. [Installation](#4-installation)
5. [Usage](#5-usage)
6. [Language Syntax](#6-language-syntax)
7. [Testing](#7-testing)
8. [Contributing](#8-contributing)
9. [License](#9-license)

---

## 1. Project Overview

**PenguinBubbleCompiler** transforms PenguinBubble (`.pg`) scripts into Python (`.py`) code. By interpreting custom commands and control structures, it enables users to write code in a simplified or domain-specific language that is then compiled into standard Python code for execution.

## 2. Features

- **Custom Commands:**
  - `penguinSay`: Print messages to the console.
  - `penguinTake`: Take user input.
  - `penguinDo`: Define functions.
  - `keepWalking`: Implement `while` loops.
  - `penguinIf`, `penguinWhatAbout`, `penguinElse`: Implement `if`, `elif`, and `else` statements.
  - Custom arithmetic operations like `slideUp`, `slideDown`, etc.

- **Modular Architecture:** 
  - Separate components for tokenization, parsing, and code generation.
  
- **Comprehensive Testing:** 
  - Unit tests for each compiler component ensuring reliability.
```bash    
python -m unittest tests/test_compiler.py
```


- **Extensible Design:** 
  - Easily add new commands and features.

## 3. Directory Structure
  - penguin_bubble_compiler/
  - │
  - ├── main.py
  - ├── compiler/
  - │   ├── __init__.py
  - │   ├── tokens.py
  - │   ├── utils.py
  - │   ├── parser.py
  - │   ├── tokenizer.py
  - │   ├── code_generator.py
  - │   └── compiler.py
  - ├── dynamic_input.py
  - ├── README.md
  - └── tests/
  -     ├── __init__.py
  -     ├── test_tokenizer.py
  -     ├── test_parser.py
  -     ├── test_code_generator.py
  -     └── test_compiler.py


**Explanation of Components:**

- **`main.py`**: Entry point of the compiler. Handles command-line interactions.
- **`compiler/`**: Core components of the compiler.
    - **`__init__.py`**: Marks the `compiler` directory as a Python package.
    - **`tokens.py`**: Defines token types.
    - **`utils.py`**: Contains utility functions (e.g., indentation handling).
    - **`parser.py`**: Handles syntax validation and potentially AST construction.
    - **`tokenizer.py`**: Implements the tokenizer (lexer).
    - **`code_generator.py`**: Translates tokens into Python code.
    - **`compiler.py`**: Integrates tokenizer and code generator to perform compilation.
    - **`README.md`**: This documentation file.
    - **`tests/`**: Contains unit tests for each compiler component.
    - **`__init__.py`**: Marks the `tests` directory as a Python package.
    - **`test_tokenizer.py`**: Tests the tokenizer.
    - **`test_parser.py`**: Tests the parser.
    - **`test_code_generator.py`**: Tests the code generator.
    - **`test_compiler.py`**: Tests the overall compilation process.

## 4. Installation

### 4.1. Prerequisites

- **Python 3.6+**: Ensure Python is installed on your system. Download it from [python.org](https://www.python.org/downloads/).

### 4.2. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/penguin_bubble_compiler.git
cd penguin_bubble_compiler