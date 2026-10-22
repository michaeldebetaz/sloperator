import pytest

from sloperator.errors import LexicalError
from sloperator.lexer import tokenize


@pytest.mark.parametrize(
    ("source", "line", "message"),
    [
        ("x @ y", 1, "unexpected character '@'"),
        ("\n\n#", 3, "unexpected character '#'"),
        ("a % b", 1, "unexpected character '%'"),
    ],
)
def test_unrecognized_character_raises_generic_error(source: str, line: int, message: str):
    with pytest.raises(LexicalError) as info:
        tokenize(source)
    assert info.value.line == line
    assert info.value.message == message
    assert str(info.value) == f"SlopLang lexical error at line {line}: {message}"
