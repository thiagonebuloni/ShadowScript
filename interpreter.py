from tokens import Integer, Float


class Interpreter:
    def __init__(self, tree, base):
        self.tree = tree
        self.data = base

    def read_INT(self, value):
        return int(value)

    def read_FLT(self, value):
        return float(value)

    def read_VAR(self, id):
        variable = self.data.read(id)
        variable_type = variable.type

        return getattr(self, f"read_{variable_type}")(variable.value)

    def compute_bin(self, left, op, right):
        left_type = "VAR" if str(left.type).startswith("VAR") else str(left.type)
        right_type = "VAR" if str(right.type).startswith("VAR") else str(right.type)

        if op.value == "=":
            left.type = f"VAR({right_type})"
            self.data.write(left, right)
            return self.data.read_all()

        left = getattr(self, f"read_{left_type}")(left.value)
        right = getattr(self, f"read_{right_type}")(right.value)

        output = None
        if op.value == "+":
            output = left + right
        elif op.value == "-":
            output = left - right
        elif op.value == "*":
            output = left * right
        elif op.value == "/":
            output = left / right
        elif op.value == ">":
            output = 1 if left > right else 0
        elif op.value == ">=":
            output = 1 if left >= right else 0
        elif op.value == "<":
            output = 1 if left < right else 0
        elif op.value == "<=":
            output = 1 if left >= right else 0
        elif op.value == "?=":
            output = 1 if left == right else 0
        elif op.value == "and":
            output = 1 if left and right else 0
        elif op.value == "or":
            output = 1 if left or right else 0

        return (
            Integer(output)
            if (left_type == "INT" and right_type == "INT")
            else Float(output)
        )

    def compute_unary(self, operator, operand):
        operand_type = (
            "VAR" if str(operand.type).startswith("VAR") else str(operand.type)
        )
        operand = getattr(self, f"read_{operand_type}")(operand.value)

        if operator.value == "+":
            return +operand
        elif operator.value == "-":
            return -operand
        elif operator.value == "not":
            return 1 if not operand else 0

    def interpret(self, tree=None):
        if tree is None:
            tree = self.tree

        # Unary operation
        if isinstance(tree, list) and len(tree) == 2:
            expression = tree[1]
            if isinstance(expression, list):
                expression = self.interpret(expression)
            return self.compute_unary(tree[0], expression)

        # No operation
        elif not isinstance(tree, list):
            return tree

        else:
            # Evaluating left subtree
            left_node = tree[0]

            if isinstance(left_node, list):
                left_node = self.interpret(left_node)

            # Evaluating right subtree
            right_node = tree[2]  # right subtree
            if isinstance(right_node, list):
                right_node = self.interpret(right_node)

            operator = tree[1]  # root node

            return self.compute_bin(left_node, operator, right_node)

    #     A
    #    / \
    #   B   C
