import pytest

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("1 < 2 == ✅", "✅"),  # (1 < 2) == ✅
        ("1 == 2 < 3", "❌"),  # 1 == (2 < 3)
        ("3 > 2 == ✅", "✅"),
        ("2 < 1 == ❌", "✅"),
    ],
)
def test_comparison_binds_tighter_than_equality(expression: str, expected: str):
    assert run(f"hallucinate({expression})✨") == f"{expected}\n"
