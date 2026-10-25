from sloperator.runner import run_source


def test_ralph_with_false_condition_prints_nothing():
    result = run_source("ralph ❌ {\n    hallucinate(“never”)✨\n}")
    assert result.stdout == ""
    assert result.stderr == ""
    assert result.exit_code == 0
