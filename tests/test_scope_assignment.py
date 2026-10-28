from sloperator.runner import run_source


def test_assignment_updates_nearest_enclosing_scope():
    source = (
        "slop score = 1✨\n"
        "{\n"
        "    slop score = 2✨\n"
        "    {\n"
        "        score = 3✨\n"
        "    }\n"
        "    hallucinate(score)✨\n"
        "}\n"
        "hallucinate(score)✨\n"
    )

    result = run_source(source)
    assert result.stderr == ""
    assert result.stdout == "3\n1\n"


def test_nested_block_sees_enclosing_block_locals():
    source = (
        "{\n"
        "    slop outer = 1✨\n"
        "    {\n"
        "        {\n"
        "            outer = outer + 1✨\n"
        "        }\n"
        "        hallucinate(outer)✨\n"
        "    }\n"
        "}\n"
    )

    result = run_source(source)
    assert result.stderr == ""
    assert result.stdout == "2\n"
