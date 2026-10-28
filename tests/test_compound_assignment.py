from sloperator.runner import run_source


def test_plus_equal_adds_evaluated_right_hand_side():
    source = "slop n = 2✨\nn += 3 * 4✨\nhallucinate(n)✨\n"

    result = run_source(source)
    assert result.stderr == ""
    assert result.stdout == "14\n"


def test_plus_equal_accepts_negative_values():
    source = "slop n = 10✨\nn += -3✨\nhallucinate(n)✨\n"

    result = run_source(source)
    assert result.stderr == ""
    assert result.stdout == "7\n"


def test_plus_equal_reads_variable_after_right_hand_side():
    source = "slop n = 2✨\nn += n✨\nhallucinate(n)✨\n"

    result = run_source(source)
    assert result.stderr == ""
    assert result.stdout == "4\n"


def test_plus_equal_sees_assignment_made_by_called_clanker():
    source = (
        "slop n = 1✨\n"
        "clanker bump() {\n"
        "    n = 100✨\n"
        "    ship 1✨\n"
        "}\n"
        "n += bump()✨\n"
        "hallucinate(n)✨\n"
    )

    result = run_source(source)
    assert result.stderr == ""
    assert result.stdout == "101\n"


def test_plus_equal_concatenates_strings():
    source = "slop s = “foo”✨\ns += “bar”✨\nhallucinate(s)✨\n"

    result = run_source(source)
    assert result.stderr == ""
    assert result.stdout == "foobar\n"


def test_plus_equal_updates_nearest_enclosing_scope():
    source = (
        "slop n = 1✨\n"
        "{\n"
        "    slop n = 5✨\n"
        "    {\n"
        "        n += 1✨\n"
        "    }\n"
        "    hallucinate(n)✨\n"
        "}\n"
        "hallucinate(n)✨\n"
    )

    result = run_source(source)
    assert result.stderr == ""
    assert result.stdout == "6\n1\n"


def test_plus_equal_updates_outer_variable_from_inner_block():
    source = "slop n = 1✨\n{\n    n += 4✨\n}\nhallucinate(n)✨\n"

    result = run_source(source)
    assert result.stderr == ""
    assert result.stdout == "5\n"


def test_plus_equal_in_loop_accumulates():
    source = (
        "slop i = 0✨\n"
        "slop total = 0✨\n"
        "ralph i < 4 {\n"
        "    total += i✨\n"
        "    i += 1✨\n"
        "}\n"
        "hallucinate(total)✨\n"
    )

    result = run_source(source)
    assert result.stderr == ""
    assert result.stdout == "6\n"


def test_plus_equal_on_undefined_name_is_runtime_error():
    source = "slop n = 1✨\nmissing += 1✨\n"

    result = run_source(source)
    assert result.stdout == ""
    assert result.stderr == "SlopLang runtime error at line 2: undefined variable 'missing'\n"
    assert result.exit_code == 1


def test_plus_equal_on_loadbearing_is_runtime_error():
    source = "loadbearing n = 1✨\nn += 1✨\n"

    result = run_source(source)
    assert result.stdout == ""
    assert result.stderr == "SlopLang runtime error at line 2: cannot assign to loadbearing 'n'\n"
    assert result.exit_code == 1


def test_plus_equal_reports_immutability_before_type_mismatch():
    source = "loadbearing s = “a”✨\ns += 1✨\n"

    result = run_source(source)
    assert result.stderr == "SlopLang runtime error at line 2: cannot assign to loadbearing 's'\n"


def test_plus_equal_number_and_string_is_runtime_error():
    source = "slop n = 1✨\nn += “a”✨\n"

    result = run_source(source)
    assert result.stdout == ""
    assert result.stderr == (
        "SlopLang runtime error at line 2: operands of '+=' must both be numbers "
        "or both be strings, got number and string\n"
    )
    assert result.exit_code == 1


def test_plus_equal_string_and_number_is_runtime_error():
    source = "slop s = “a”✨\ns += 1✨\n"

    result = run_source(source)
    assert result.stderr == (
        "SlopLang runtime error at line 2: operands of '+=' must both be numbers "
        "or both be strings, got string and number\n"
    )


def test_plus_equal_boolean_is_runtime_error():
    source = "slop n = 1✨\nn += ✅✨\n"

    result = run_source(source)
    assert result.stderr == (
        "SlopLang runtime error at line 2: operands of '+=' must both be numbers "
        "or both be strings, got number and boolean\n"
    )


def test_plus_equal_nil_is_runtime_error():
    source = "clanker f() {\n}\nslop n = 1✨\nn += f()✨\n"

    result = run_source(source)
    assert result.stderr == (
        "SlopLang runtime error at line 4: operands of '+=' must both be numbers "
        "or both be strings, got number and nil\n"
    )


def test_plus_equal_undefined_name_in_right_hand_side_is_runtime_error():
    source = "slop n = 1✨\nn += missing✨\n"

    result = run_source(source)
    assert result.stderr == "SlopLang runtime error at line 2: undefined variable 'missing'\n"
