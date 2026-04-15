# dotxc.py
from parser import parser
from lexer import lexer

test_code = """
strict graph { 
  a -- b
  a -- b
  b -- a [color=blue]
} 
"""

print("Rozpoczynam analizę składniową...")
ast_tree = parser.parse(test_code, lexer=lexer)

print("\nWygenerowane drzewo AST:")
print(ast_tree)