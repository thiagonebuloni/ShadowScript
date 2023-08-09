from tokens import (
    Integer,
    Float,
    Operation,
    Declaration,
    Variable,
    Boolean,
    Comparison,
    Reserved,
)


class Lexer:
    digits = "0123456789"
    letters = "abcdefghijklmnopqrstuvwxyz"
    operations = "+-/*()="
    stopwords = [" "]
    declarations = ["make"]
    boolean = ["and", "or", "not"]
    comparisons = [">", "<", ">=", "<=", "?="]
    special_characters = "><=?"
    reserved = ["if", "elif", "else", "do", "while"]

    def __init__(self, text: str) -> None:
        self.text: str = text
        self.idx: int = 0
        self.tokens: list = []
        self.char: str = self.text[self.idx]
        self.token = None

    def tokenize(self) -> list:
        while self.idx < len(self.text):
            if self.char in Lexer.digits:
                self.token = self.extract_number()

            elif self.char in Lexer.operations:
                self.token = Operation(self.char)
                self.move()

            elif self.char in Lexer.stopwords:
                self.move()
                continue

            elif self.char in Lexer.letters:
                word: str = self.extract_word()

                self.token = self.word_in_letters(word)

            elif self.char in Lexer.special_characters:
                comparison_operator = ""
                while self.char in Lexer.special_characters and self.idx < len(
                    self.text
                ):
                    comparison_operator += self.char
                    self.move()

                self.token = Comparison(comparison_operator)

            self.tokens.append(self.token)

        return self.tokens

    def word_in_letters(self, word: str) -> Declaration | Boolean | Reserved | Variable:
        if word in Lexer.declarations:
            self.token = Declaration(word)
        elif word in Lexer.boolean:
            self.token = Boolean(word)
        elif word in Lexer.reserved:
            self.token = Reserved(word)
        else:
            self.token = Variable(word)
        return self.token

    def extract_number(self) -> Integer | Float:
        number = ""
        is_float = False
        while (self.char in Lexer.digits or self.char == ".") and (
            self.idx < len(self.text)
        ):
            if self.char == ".":
                is_float = True
            number += self.char
            self.move()

        return Integer(number) if not is_float else Float(number)

    def extract_word(self) -> str:
        word = ""
        while self.char in Lexer.letters and self.idx < len(self.text):
            word += self.char
            self.move()

        return word

    def move(self) -> None:
        self.idx += 1
        if self.idx < len(self.text):
            self.char = self.text[self.idx]
