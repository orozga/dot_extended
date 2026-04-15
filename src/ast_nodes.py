from tokens import tokens, reserved


class Node:
    def __init__(self, node_type, value=None, children=None):
        self.node_type = node_type
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        return f"Node(type={self.node_type}, value={self.value}, children={self.children})"


class ComponentNode:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"ComponentNode(name={self.name}, params={self.params}, body={self.body})"


class GraphNode:
    def __init__(self, name, graph_type, is_strict, body):
        self.name = name
        self.graph_type = graph_type
        self.is_strict = is_strict
        self.body = body

    def __repr__(self):
        return f"GraphNode(name={self.name}, body={self.body})"


class SubgraphNode:
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def __repr__(self):
        return f"SubgraphNode(name={self.name}, body={self.body})"


class ShortcutDefNode:
    def __init__(self, symbol, params, body):
        self.symbol = symbol
        self.params = params
        self.body = body

    def __repr__(self):
        return f"ShortcutDefNode(symbol={self.symbol}, params={self.params}, body={self.body})"


class AttributeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return f"AttributeNode(key={self.key}, value={self.value})"


class GlobalAttributeNode:
    def __init__(self, target_type, attributes):
        self.target_type = target_type
        self.attributes = attributes

    def __repr__(self):
        return f"GlobalAttributeNode(target_type={self.target_type}, attributes={self.attributes})"


class NodeCallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"NodeCallNode(name={self.name}, args={self.args})"


class EdgeNode:
    def __init__(self, source, target, operator, attributes=None):
        self.source = source
        self.target = target
        self.operator = operator
        self.attributes = attributes if attributes is not None else []

    def __repr__(self):
        return f"EdgeNode(source={self.source}, target={self.target}, operator={self.operator}, attributes={self.attributes})"
