import pytest

from sloperator.runner import run_source


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("hallucinate(“” + “slop”)✨", "slop\n"),
        ("hallucinate(“slop” + “”)✨", "slop\n"),
        ("hallucinate(“” + “”)✨", "\n"),
        ("hallucinate(“café” + “✨”)✨", "café✨\n"),
        ("hallucinate(“hal” + “lu” + “cinate”)✨", "hallucinate\n"),
        ("hallucinate(“a\\n” + “b”)✨", "a\nb\n"),
    ],
)
def test_string_addition(source: str, expected: str):
    result = run_source(source)
    assert result.stderr == ""
    assert result.stdout == expected


def test_string_addition_with_variables():
    source = """
slop name = “slop”✨
slop greeting = “” + name✨
hallucinate(greeting + “!”)✨
"""
    result = run_source(source)
    assert result.stderr == ""
    assert result.stdout == "slop!\n"
