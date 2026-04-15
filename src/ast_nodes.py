from tokens import tokens, reserved

class ASTNode:
    def __init__(self, node_type, value=None, children=None):
        self.node_type = node_type
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        return f"ASTNode(type={self.node_type}, value={self.value}, children={self.children})"
    

class ComponentNode(ASTNode):
    def __init__(self, name, params, body):
        super().__init__('Component', children=body)
        self.name = name
        self.params = params

    def __repr__(self):
        return f"ComponentNode(name={self.name}, params={self.params}, body={self.children})"
    
class GraphNode(ASTNode):
    def __init__(self, name, graph_type, is_strict, body):
        super().__init__('Graph')
        self.name = name
        self.graph_type = graph_type
        self.is_strict = is_strict
        self.body = body

    def __repr__(self):
        return f"GraphNode(name={self.name}, body={self.body})"
    
class ShortcutDefNode(ASTNode):
    def __init__(self, symbol, params, body):
        super().__init__('Shortcut')
        self.symbol = symbol
        self.params = params
        self.body = body

    def __repr__(self):
        return f"ShortcutDefNode(symbol={self.symbol}, params={self.params}, body={self.body})"
    
class AttributeNode(ASTNode):
    def __init__(self, key, value):
        super().__init__('Attribute')
        self.key = key
        self.value = value

    def __repr__(self):
        return f"AttributeNode(key={self.key}, value={self.value})"

class NodeCallNode(ASTNode):
    def __init__(self, name, args):
        super().__init__('NodeCall')
        self.name = name
        self.args = args

    def __repr__(self):
        return f"NodeCallNode(name={self.name}, args={self.args})"

class EdgeNode(ASTNode):
    def __init__(self, source, target, operator, attributes=None):
        super().__init__('Edge')
        self.source = source
        self.target = target
        self.operator = operator
        self.attributes = attributes if attributes is not None else []

    def __repr__(self):
        return f"EdgeNode(source={self.source}, target={self.target}, operator={self.operator}, attributes={self.attributes})"