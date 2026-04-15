reserved = {
    'component': 'KW_COMPONENT',
    'defshortcut': 'KW_DEFSHORTCUT',
    'digraph': 'KW_DIGRAPH',
    'strict': 'KW_STRICT',
    'graph': 'KW_GRAPH'
}

tokens = (
    'ID',
    'VAR_ID',
    'STRING',
    'ARROW',
    'FAT_ARROW',
    'CUSTOM_OP',
    'LBRACE',
    'RBRACE',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'EQUALS',
    'SEMICOLON',
) + tuple(reserved.values())