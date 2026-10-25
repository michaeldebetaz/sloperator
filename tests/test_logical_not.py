import pytest

from sloperator.runner import run_source


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("hallucinate(!✅)✨", "❌\n"),
        ("hallucinate(!❌)✨", "✅\n"),
        ("hallucinate(!!✅)✨", "✅\n"),
        ("hallucinate(!!!✅)✨", "❌\n"),
        ("hallucinate(!(✅ && ❌))✨", "✅\n"),
        ("hallucinate(!❌ || ❌)✨", "✅\n"),
        ("hallucinate(!✅ == ❌)✨", "✅\n"),
        ("hallucinate(!✅, !❌, !!✅)✨", "❌ ✅ ✅\n"),
    ],
)
def test_logical_not(source: str, expected: str):
    result = run_source(source)
    assert result.stderr == ""
    assert result.stdout == expected


@pytest.mark.parametrize(
    ("operand", "type_name"),
    [("1", "number"), ("“a”", "string"), ("nothing()", "nil")],
)
def test_logical_not_rejects_non_booleans(operand: str, type_name: str):
    source = f"clanker nothing() {{ }}\nhallucinate(!{operand})✨"
    result = run_source(source)
    assert result.stdout == ""
    assert result.exit_code == 1
    assert result.stderr.rstrip("\n") == (
        f"SlopLang runtime error at line 2: operand of unary '!' must be a boolean, got {type_name}"
    )
