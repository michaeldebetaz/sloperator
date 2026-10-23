import pytest

from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt, Literal
from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("1 + 2 * 3", "7"),
        ("2 * 3 + 1", "7"),
        ("1 + 2 * 3 + 4 * 5", "27"),
        ("10 - 2 * 3", "4"),
        ("(1 + 2) * 3", "9"),
    ],
)
def test_multiplication_binds_tighter_than_addition(expression: str, expected: str):
    assert run(f"hallucinate({expression})✨") == f"{expected}\n"


def test_addition_keeps_multiplication_as_its_right_operand():
    (statement,) = parse(tokenize("1 + 2 * 3✨"))
    assert isinstance(statement, ExprStmt)
    expression = statement.expression
    assert isinstance(expression, Binary)
    assert expression.operator.type is TokenType.PLUS
    assert isinstance(expression.left, Literal) and expression.left.value == 1
    assert isinstance(expression.right, Binary)
    assert expression.right.operator.type is TokenType.STAR
