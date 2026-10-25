"""Exact stdout for example programs that exercise specific language features."""

from pathlib import Path

import pytest

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"

CASES = {
    "equality.slop": "✅\n❌\n❌\n",
}


@pytest.mark.parametrize("name", CASES)
def test_example_output(name: str):
    result = run_source((EXAMPLES / name).read_text(encoding="utf-8"))
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == CASES[name]
