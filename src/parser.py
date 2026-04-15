import ply.yacc as yacc
from tokens import tokens
from ast_nodes import *

def p_program(p):
    '''program : top_level_list'''
    p[0] = p[1]

def p_top_level_list(p):
    '''top_level_list : top_level_list top_level_stmt
                      | top_level_stmt'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_top_level_stmt(p):
    '''top_level_stmt : component_def
                      | shortcut_def
                      | graph_def'''
    p[0] = p[1]

def p_graph_def(p):
    '''graph_def : strict_opt graph_type id_opt LBRACE graph_body RBRACE'''
    p[0] = GraphNode(name=p[3], graph_type=p[2], is_strict=p[1], body=p[5])

def p_component_def(p):
    '''component_def : KW_COMPONENT ID LPAREN param_list RPAREN LBRACE graph_body RBRACE'''
    p[0] = ComponentNode(name=p[2], params=p[4], body=p[7])

def p_param_list(p):
    '''param_list : ID COMMA param_list
                  | ID
                  | empty'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_shortcut_def(p):
    '''shortcut_def : KW_DEFSHORTCUT CUSTOM_OP FAT_ARROW edge_op attr_block_opt semi_opt'''
    p[0] = ShortcutDefNode(symbol=p[2], params=p[4], body=p[5])

def p_graph_type(p):
    '''graph_type : KW_GRAPH
                  | KW_DIGRAPH'''
    p[0] = p[1]

def p_id_opt(p):
    '''id_opt : ID
              | empty'''
    p[0] = p[1] if p[1] else None

def p_graph_body(p):
    '''graph_body : graph_body statement
                  | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_node_id(p):
    '''node_id : ID
               | VAR_ID'''
    p[0] = p[1]

def p_edge_op(p):
    '''edge_op : ARROW
               | EDGE_UNDIR
               | CUSTOM_OP'''
    p[0] = p[1]

def p_subgraph(p):
    '''subgraph : KW_SUBGRAPH id_opt LBRACE graph_body RBRACE
                | LBRACE graph_body RBRACE'''
    if len(p) == 6:
        p[0] = SubgraphNode(name=p[2], body=p[4])
    elif len(p) == 4:
        p[0] = SubgraphNode(name=None, body=p[2])

def p_global_type(p):
    '''global_type : KW_NODE
                   | KW_EDGE
                   | KW_GRAPH'''
    p[0] = p[1]

def p_statement(p):
    '''statement : node_id edge_op node_id attr_block_opt semi_opt
                 | node_id attr_block_opt semi_opt
                 | node_id LPAREN arg_list RPAREN semi_opt
                 | subgraph
                 | global_type attr_block_opt semi_opt'''
    if len(p) == 6:
        if p.slice[2].type == "edge_op":
            p[0] = EdgeNode(source=Node(node_type="Node", value=p[1]), target=Node(node_type="Node", value=p[3]), operator=p[2], attributes=p[4])
        else:
            p[0] = NodeCallNode(name=p[1], args=p[3])
    elif len(p) == 4:
        if p.slice[1].type == "node_id":
            p[0] = Node(node_type="Node", value=p[1], children=p[2])
        else:
            p[0] = GlobalAttributeNode(target_type=p[1], attributes=p[2])
    elif len(p) == 2:
        p[0] = p[1]

def p_semi_opt(p):
    '''semi_opt : SEMICOLON
                | empty'''
    pass

def p_value(p):
    '''value : ID
             | STRING
             | VAR_ID
             | NUMBER'''   
    p[0] = p[1]

def p_arg_list(p):
    '''arg_list : value COMMA arg_list
                | value
                | empty'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_attr(p):
    '''attr : ID EQUALS value'''
    p[0] = AttributeNode(key=p[1], value=p[3])

def p_attr_list(p):
    '''attr_list : attr COMMA attr_list
                 | attr'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_attr_block_opt(p):
    '''attr_block_opt : LBRACKET attr_list RBRACKET
                      | empty'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []

def p_strict_opt(p):
    '''strict_opt : KW_STRICT
                  | empty'''
    p[0] = p[1] == "strict"

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        print(f"Błąd składniowy: nieoczekiwany token '{p.value}'")
    else:
        print("Błąd składniowy: nieoczekiwany koniec pliku")

parser = yacc.yacc()