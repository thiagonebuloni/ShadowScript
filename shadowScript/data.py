class Data:
    def __init__(self) -> None:
        self.variables = {}

    def read(self, id: int) -> dict:
        return self.variables[id]

    def read_all(self) -> dict:
        return self.variables

    def write(self, variable, expression: int | float) -> None:
        variable_name = variable.value
        self.variables[variable_name] = expression
