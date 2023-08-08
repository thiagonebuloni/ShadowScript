from tokens import Integer, Float, Reserved, Token
from numbers import Number
from typing import Literal


class Interpreter:
    operations = "+-/*()="
    boolean = ["and", "or", "not"]
    comparisons = [">", "<", ">=", "<=", "?="]

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

    def compute_calculations(
        self, left: int | float, op: Token, right: int | float
    ) -> int | float | Literal["", "Impossible zero division"]:
        output = ""
        if op.value == "+":
            output = left + right
        elif op.value == "-":
            output = left - right
        elif op.value == "*":
            output = left * right
        elif op.value == "/":
            if left == 0 or right == 0:
                return "Impossible zero division"
            output = left / right
        return output

    def compute_boolean_operations(
        self, left: int | float, op: Token, right: int | float
    ) -> Literal[1, 0, ""]:
        output = ""
        if op.value == "and":
            output = 1 if left and right else 0
        elif op.value == "or":
            output = 1 if left or right else 0
        return output

    def compute_comparisons(
        self, left: int | float, op: Token, right: int | float
    ) -> Literal[1, 0, ""]:
        output = ""
        if op.value == ">":
            output = 1 if left > right else 0
        elif op.value == ">=":
            output = 1 if left >= right else 0
        elif op.value == "<":
            output = 1 if left < right else 0
        elif op.value == "<=":
            output = 1 if left >= right else 0
        elif op.value == "?=":
            output = 1 if left == right else 0
        return output

    def compute_bin(self, left: Token, op: Token, right: Token) -> Integer | Float:
        left_type = "VAR" if str(left.type).startswith("VAR") else str(left.type)
        right_type = "VAR" if str(right.type).startswith("VAR") else str(right.type)

        if op.value == "=":
            left.type = f"VAR({right_type})"
            self.data.write(left, right)
            return self.data.read_all()

        left = getattr(self, f"read_{left_type}")(left.value)
        right = getattr(self, f"read_{right_type}")(right.value)

        if op.value in Interpreter.operations:
            output = self.compute_calculations(left, op, right)
        elif op.value in Interpreter.boolean:
            output = self.compute_boolean_operations(left, op, right)
        else:
            output = self.compute_comparisons(left, op, right)

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

        output = None
        if operator.value == "+":
            output = +operand
        elif operator.value == "-":
            output = -operand
        elif operator.value == "not":
            output = 1 if not operand else 0

        return Integer(output) if (operand_type == "INT") else Float(output)

    def interpret(self, tree=None):
        if tree is None:
            tree = self.tree

        if isinstance(tree, list) and isinstance(tree[0], Reserved):
            if tree[0].value == "if":
                for idx, condition in enumerate(tree[1][0]):
                    evaluation = self.interpret(condition)
                    # https://github.com/microsoft/pylance-release/issues/1785#issuecomment-915576918
                    assert evaluation is not None

                    if evaluation.value == 1:
                        return self.interpret(tree[1][1][idx])

                if len(tree[1]) == 3:
                    return self.interpret(tree[1][2])

                else:
                    return

            elif tree[0].value == "while":
                condition = self.interpret(tree[1][0])
                # https://github.com/microsoft/pylance-release/issues/1785#issuecomment-915576918
                assert condition is not None

                while condition.value == 1:
                    # Doing the action
                    print(self.interpret(tree[1][1]))

                    # Checking the condition
                    condition = self.interpret(tree[1][0])

                return

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
