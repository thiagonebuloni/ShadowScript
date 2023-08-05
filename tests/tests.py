from shadowScript.tokens import Token
from shadowScript.lexer import Lexer
from shadowScript.parse import Parser
from shadowScript.interpreter import Interpreter
from shadowScript.data import Data


def base_shadow_script(text: str):
    base = Data()
    tokenizer = Lexer(text)
    tokens = tokenizer.tokenize()

    parser = Parser(tokens)
    tree = parser.parse()

    interpreter = Interpreter(tree, base)
    result = interpreter.interpret()
    return result


def test_add():
    text = "2 + 2"
    result = base_shadow_script(text)
    assert result.value == 4  # type: ignore


def test_add_zero():
    text = "0 + 0"
    result = base_shadow_script(text)
    assert result.value == 0  # type: ignore


def test_add_float():
    text = "2.0 + 2"
    result = base_shadow_script(text)
    assert result.value == 4.0  # type: ignore


def test_subtraction():
    text = "2 - 2"
    result = base_shadow_script(text)
    assert result.value == 0  # type: ignore


def test_subtraction_with_zero():
    text = "0 - 0"
    result = base_shadow_script(text)
    assert result.value == 0  # type: ignore


def test_subtraction_float():
    text = "2.0 - 2"
    result = base_shadow_script(text)
    assert result.value == 0  # type: ignore


def test_subtraction_with_negative_result():
    text = "2 - 3"
    result = base_shadow_script(text)
    assert result.value == -1  # type: ignore


def test_multiplication():
    text = "2 * 2"
    result = base_shadow_script(text)
    assert result.value == 4  # type: ignore


def test_multiplication_with_zero():
    text = "2 * 0"
    result = base_shadow_script(text)
    assert result.value == 0  # type: ignore


def test_multiplication_float():
    text = "2 * 2.0"
    result = base_shadow_script(text)
    assert result.value == 4.0  # type: ignore


def test_mulplication_with_sum():
    text = "2 * 2 + 3"
    result = base_shadow_script(text)
    assert result.value == 7  # type: ignore


def test_sum_with_mulplication():
    text = "2 * (2 + 3)"
    result = base_shadow_script(text)
    assert result.value == 10  # type: ignore


def test_division():
    text = "2 / 2"
    result = base_shadow_script(text)
    assert result.value == 1  # type: ignore


def test_division_float():
    text = "2 / 1"
    result = base_shadow_script(text)
    assert result.value == 2.0  # type: ignore


def test_division_with_sum():
    text = "2 / 2 + 3"
    result = base_shadow_script(text)
    assert result.value == 4  # type: ignore


def test_sum_with_division():
    text = "6 / (2 + 4)"
    result = base_shadow_script(text)
    assert result.value == 1  # type: ignore


def test_assign_variable():
    text = "make a = 0"
    result = base_shadow_script(text)
    assert result["a"].value == "0"  # type: ignore


def test_operator_and():
    text = "2 > 0 and 2 < 4"
    result = base_shadow_script(text)
    assert result.value == 1  # type: ignore


def test_operator_or():
    text = "2 > 0 or 2 > 4"
    result = base_shadow_script(text)
    assert result.value == 1  # type: ignore


def test_operator_not():
    text = "not 2 > 0"
    result = base_shadow_script(text)
    assert result.value == 1  # type: ignore
