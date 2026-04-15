import ply.lex as lex

from tokens import tokens, reserved

def t_ARROW(t):
    r'->'
    return t
def t_FAT_ARROW(t):
    r'=>'
    return t
def t_SEMICOLON(t):
    r';'
    return t
def t_LBRACE(t):
    r'\{'
    return t
def t_RBRACE(t):
    r'\}'
    return t
def t_LPAREN(t):
    r'\('
    return t
def t_RPAREN(t):
    r'\)'
    return t
def t_LBRACKET(t):
    r'\['
    return t
def t_RBRACKET(t):
    r'\]'
    return t
def t_COMMA(t):
    r','
    return t
def t_EQUALS(t):
    r'='
    return t
def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1].encode().decode('unicode_escape')
    return t
def t_VAR_ID(t):
    r'\$[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_CUSTOM_OP(t):
    r'<[a-zA-Z0-9_\.\-]*>'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

t_ignore  = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Błąd leksykalny: Nierozpoznany znak '{t.value[0]}' w linii {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()