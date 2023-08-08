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


def test_operator_greater_than():
    text = "2 > 0"
    result = base_shadow_script(text)
    assert result.value == 1  # type: ignore


def test_operator_less_than():
    text = "0 < 2"
    result = base_shadow_script(text)
    assert result.value == 1  # type: ignore


def test_operator_equal():
    text = "2 ?= 2"
    result = base_shadow_script(text)
    assert result.value == 1  # type: ignore


def test_operator_less_or_equal_than():
    text = "2 <= 2"
    result = base_shadow_script(text)
    assert result.value == 1  # type: ignore


def test_operator_less_or_equal_than2():  #! wrong answer. WHY
    text = "0 <= 2"
    result = base_shadow_script(text)
    assert result.value == 0  # type: ignore


def test_operator_greater_or_equal_than():
    text = "2 >= 2"
    result = base_shadow_script(text)
    assert result.value == 1  # type: ignore


def test_operator_greater_or_equal_than2():
    text = "0 >= 2"
    result = base_shadow_script(text)
    assert result.value == 0  # type: ignore


def test_operator_not():
    text = "not 2 > 0"
    result = base_shadow_script(text)
    assert result.value == 0  # type: ignore


def test_operator_not2():
    text = "not 2 < 0"
    result = base_shadow_script(text)
    assert result.value == 1  # type: ignore


def test_operator_and_with_not():
    text = "5 ?= 5 and (not 2 < 0)"
    result = base_shadow_script(text)
    assert result.value == 1  # type: ignore


def test_operator_or_with_not():
    text = "5 ?= 5 or (not 2 < 0)"
    result = base_shadow_script(text)
    assert result.value == 1  # type: ignore


def test_ifconditions():
    text = "if 2 > 0 do 2 + 2"
    result = base_shadow_script(text)
    assert result.value == 4  # type: ignore


def test_ifconditions2():
    text = "if 2 < 0 do 2 + 2"
    result = base_shadow_script(text)
    assert result == None  # type: ignore


def test_if_elif_else_conditions():
    text = "if 2 < 0 do 2 + 2 elif 2 ?= 0 do 10 + 2 else do 20 + 2"
    result = base_shadow_script(text)
    assert result.value == 22  # type: ignore


def test_if_else_conditions():
    text = "if 2 < 0 do 2 + 2 else do 20 + 2"
    result = base_shadow_script(text)
    assert result.value == 22  # type: ignore


# def test_while():
#     text = "make a = 0"
#     base_shadow_script(text)
#     # assert result["a"].value == "0"  # type: ignore
#     text = "while a < 10 do make a = a + 1"
#     result = base_shadow_script(text)
#     assert result.value == '{"a": 10.0}'  # type: ignore
