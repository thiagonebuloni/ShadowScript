class Parser:
    def __init__(self, tokens: list) -> None:
        self.tokens: list = tokens
        self.idx: int = 0
        self.token = self.tokens[self.idx]

    def factor(self) -> list | None:
        if self.token.type == "INT" or self.token.type == "FLT":
            return self.token
        elif self.token.value == "(":
            self.move()
            expression = self.boolean_expression()
            return expression
        elif self.token.value == "not":
            operator = self.token
            self.move()
            output = [operator, self.boolean_expression()]
            return output

        elif self.token.type.startswith("VAR"):
            return self.token
        elif self.token.value == "+" or self.token.value == "-":
            operator = self.token
            self.move()
            operand = self.boolean_expression()

            return [operator, operand]

    def term(self) -> list[str] | None:
        left_node = self.factor()
        self.move()

        while self.token.value == "*" or self.token.value == "/":
            operator = self.token
            self.move()
            right_node = self.factor()
            self.move()

            left_node = [left_node, operator, right_node]

        return left_node

    def if_statement(self) -> tuple:
        self.move()
        condition = self.boolean_expression()

        if self.token.value == "do":
            self.move()
            action = self.statement()

            return condition, action
        elif self.tokens[self.idx - 1].value == "do":
            action = self.statement()
            return condition, action
        else:
            return ()

    def if_statements(self) -> list | list[list]:
        conditions: list = []
        actions: list = []
        if_statement: tuple = self.if_statement()

        conditions.append(if_statement[0])
        actions.append(if_statement[1])

        while self.token.value == "elif":
            if_statement = self.if_statement()
            conditions.append(if_statement[0])
            actions.append(if_statement[1])

        if self.token.value == "else":
            self.move()
            self.move()
            else_action = self.statement()

            return [conditions, actions, else_action]

        return [conditions, actions]

    def while_statement(self) -> list | None:
        self.move()
        condition = self.boolean_expression()

        if self.token.value == "do":
            self.move()
            action = self.statement()
            return [condition, action]

        elif self.tokens[self.idx - 1].value == "do":
            action = self.statement()
            return [condition, action]

    def comp_expression(self) -> list | None:
        left_node = self.expression()
        while self.token.type == "COMP":
            operation = self.token
            self.move()
            right_node = self.expression()
            left_node = [left_node, operation, right_node]

        return left_node

    def boolean_expression(self) -> list | None:
        left_node = self.comp_expression()
        while self.token.type == "BOOL":
            operation = self.token
            self.move()
            right_node = self.comp_expression()
            left_node = [left_node, operation, right_node]

        return left_node

    def expression(self) -> list[str] | None:
        left_node = self.term()
        while self.token.value == "+" or self.token.value == "-":
            operation = self.token
            self.move()
            right_node = self.term()
            left_node = [left_node, operation, right_node]

        return left_node

    def variable(self):
        if self.token.type.startswith("VAR"):
            return self.token

    def statement(self) -> list | None:
        if self.token.type == "DECL":
            # Variable assignment
            self.move()
            left_node = self.variable()
            self.move()
            if self.token.value == "=":
                operation = self.token
                self.move()
                right_node = self.boolean_expression()

                return [left_node, operation, right_node]

        elif (
            self.token.type == "INT"
            or self.token.type == "FLT"
            or self.token.type == "OP"
            or self.token.value == "not"
        ):
            # Aritmathic expression
            return self.boolean_expression()

        elif self.token.value == "if":
            return [self.token, self.if_statements()]
        elif self.token.value == "while":
            return [self.token, self.while_statement()]

    def parse(self) -> list | None:
        return self.statement()

    def move(self) -> None:
        self.idx += 1
        if self.idx < len(self.tokens):
            self.token = self.tokens[self.idx]


#       +
#      / \
#     +   4
#    / \
#   +   3
#  / \
# 1   2
