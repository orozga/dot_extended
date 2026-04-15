import ply.yacc as yacc
from tokens import tokens
from ast_nodes import *

def p_program(p):
    '''program : strict_op KW_DIGRAPH ID LBRACE graph_body RBRACE'''
    p[0] = GraphNode(name=p[2], graph_type='digraph', is_strict=p[1], body=p[4])

def p_graph_body(p):
    '''graph_body : graph_body statement
                  | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : ID ARROW ID SEMICOLON
                 | ID SEMICOLON'''
    if len(p) == 5:
        p[0] = EdgeNode(source=p[1], target=p[3], operator=p[2])
    else:
        p[0] = ASTNode(node_type='Node', value=p[1])

def p_error(p):
    if p:
        print(f"Błąd składniowy: nieoczekiwany token '{p.value}'")
    else:
        print("Błąd składniowy: nieoczekiwany koniec pliku")

def p_strict_op(p):
    '''strict_op : KW_STRICT
                 | empty'''
    p[0] = (p[1] == 'strict')

def p_empty(p):
    'empty :'
    pass

parser = yacc.yacc()