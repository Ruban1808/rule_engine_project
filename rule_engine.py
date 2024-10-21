import ast

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left  # Left child node (for operator nodes)
        self.right = right  # Right child node (for operator nodes)
        self.value = value  # Value for operand nodes (e.g., conditions)

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value})"

def create_rule(rule_string):
    """Parses a rule string and returns an AST Node."""
    tree = ast.parse(rule_string, mode='eval')
    return _build_ast(tree.body)

def _build_ast(node):
    """Helper function to build AST from Python AST nodes."""
    if isinstance(node, ast.BoolOp):
        op = "AND" if isinstance(node.op, ast.And) else "OR"
        left = _build_ast(node.values[0])
        right = _build_ast(node.values[1])
        return Node("operator", left=left, right=right, value=op)
    elif isinstance(node, ast.Compare):
        left = node.left.id
        comparator = ast.dump(node.ops[0])
        right = node.comparators[0].value if isinstance(node.comparators[0], ast.Constant) else node.comparators[0].id
        condition = f"{left} {comparator} {right}"
        return Node("operand", value=condition)

def combine_rules(rules):
    """Combines multiple AST rules into one."""
    if not rules:
        return None
    combined_ast = create_rule(rules[0])
    for rule in rules[1:]:
        new_ast = create_rule(rule)
        combined_ast = Node("operator", left=combined_ast, right=new_ast, value="AND")
    return combined_ast

def evaluate_rule(ast_node, data):
    """Evaluates the rule against provided data."""
    if ast_node.type == "operand":
        condition = ast_node.value
        return eval(condition, {}, data)
    elif ast_node.type == "operator":
        left_eval = evaluate_rule(ast_node.left, data)
        right_eval = evaluate_rule(ast_node.right, data)
        if ast_node.value == "AND":
            return left_eval and right_eval
        elif ast_node.value == "OR":
            return left_eval or right_eval
