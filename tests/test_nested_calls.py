from sloperator.lexer import tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Call, ExprStmt, Variable
from sloperator.runner import run_source


def test_call_as_argument_to_another_call():
    source = "clanker add(left, right) {\n    ship left + right✨\n}\nhallucinate(add(1, 2))✨\n"

    *_, statement = parse(tokenize(source))
    assert isinstance(statement, ExprStmt)
    outer = statement.expression
    assert isinstance(outer, Call) and isinstance(outer.callee, Variable)
    assert outer.callee.name.lexeme == "hallucinate"
    (inner,) = outer.arguments
    assert isinstance(inner, Call) and isinstance(inner.callee, Variable)
    assert inner.callee.name.lexeme == "add"
    assert len(inner.arguments) == 2

    result = run_source(source)
    assert result.stderr == ""
    assert result.stdout == "3\n"
