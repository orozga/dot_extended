from ast_nodes import NodeCallNode


class CodeGenerator:
    def __init__(self):
        self.output = ""
        self.indent = 0
        self.components = {}
        self.shortcuts = {}
        self.variables = {}

    def emit(self, text):
        self.output += "    " * self.indent + text + "\n"

    def resolve_vars(self, text):
        if not isinstance(text, str):
            return str(text)
        sorted_vars = sorted(
            self.variables.items(), key=lambda x: len(x[0]), reverse=True
        )
        for var_name, var_val in sorted_vars:
            text = text.replace(var_name, str(var_val))
        return text

    def visit(self, node):
        if node is None:
            return
        method = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        pass

    def visit_GraphNode(self, node):
        strict_str = "strict " if node.is_strict else ""
        self.emit(f"{strict_str}{node.graph_type} {node.name or ''} {{")
        self.indent += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent -= 1
        self.emit("}")

    def visit_ComponentNode(self, node):
        self.components[node.name] = node

    def visit_ShortcutDefNode(self, node):
        self.shortcuts[node.symbol] = node

    def visit_ConstNode(self, node):
        self.variables[node.name] = node.value

    def visit_ImportNode(self, node):
        pass

    def visit_Node(self, node):
        val = self.resolve_vars(node.value)
        attr_str = ""
        if node.children:
            attr_str = (
                " ["
                + ", ".join(
                    [
                        f"{self.resolve_vars(a.key)}={self.resolve_vars(a.value)}"
                        for a in node.children
                    ]
                )
                + "]"
            )
        self.emit(f"{val}{attr_str};")

    def visit_EdgeNode(self, node):
        op = node.operator
        attrs = node.attributes

        if op in self.shortcuts:
            shortcut = self.shortcuts[op]
            op = shortcut.params
            attrs = shortcut.body + attrs

        attr_str = ""
        if attrs:
            attr_str = (
                " ["
                + ", ".join(
                    [
                        f"{self.resolve_vars(a.key)}={self.resolve_vars(a.value)}"
                        for a in attrs
                    ]
                )
                + "]"
            )

        src = self.resolve_vars(node.source.value)
        tgt = self.resolve_vars(node.target.value)
        self.emit(f"{src} {op} {tgt}{attr_str};")

    def visit_AttributeNode(self, node):
        key = self.resolve_vars(node.key)
        val = self.resolve_vars(node.value)
        self.emit(f"{key} = {val};")

    def visit_GlobalAttributeNode(self, node):
        attr_str = ""
        if node.attributes:
            attr_str = (
                " ["
                + ", ".join(
                    [
                        f"{self.resolve_vars(a.key)}={self.resolve_vars(a.value)}"
                        for a in node.attributes
                    ]
                )
                + "]"
            )
        self.emit(f"{node.target_type}{attr_str};")

    def visit_SubgraphNode(self, node):
        name_str = f"subgraph {node.name} " if node.name else ""
        self.emit(f"{name_str}{{")
        self.indent += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent -= 1
        self.emit("}")

    def visit_ForLoopNode(self, node):
        start = int(node.iterable.start)
        stop = int(node.iterable.stop)
        step = int(node.iterable.step)

        old_vars = self.variables.copy()
        for val in range(start, stop + 1, step):
            self.variables[node.variable] = str(val)
            for stmt in node.body:
                self.visit(stmt)
        self.variables = old_vars

    def visit_NodeCallNode(self, node):
        if node.name in self.components:
            comp = self.components[node.name]
            old_vars = self.variables.copy()

            for i, param in enumerate(comp.params):
                if i < len(node.args):
                    self.variables[f"${param}"] = self.resolve_vars(node.args[i])

            if comp.extends:
                parent_name = comp.extends["parent"]
                parent_args = [self.resolve_vars(arg) for arg in comp.extends["args"]]
                self.visit_NodeCallNode(NodeCallNode(parent_name, parent_args))

            for stmt in comp.body:
                self.visit(stmt)

            self.variables = old_vars
