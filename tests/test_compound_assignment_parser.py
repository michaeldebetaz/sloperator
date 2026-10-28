import pytest

from sloperator.errors import SlopSyntaxError
from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Assign, Binary, Block, If, Literal, Ship, Variable, While


def parse_source(source: str):
    return parse(tokenize(source))


def only_statement(source: str):
    (statement,) = parse_source(source)
    return statement


def test_plus_equal_lexes_as_single_token():
    types = [token.type for token in tokenize("x += 1✨")]
    assert types == [
        TokenType.IDENTIFIER,
        TokenType.PLUS_EQUAL,
        TokenType.NUMBER,
        TokenType.SPARKLES,
        TokenType.EOF,
    ]


def test_plus_without_equal_is_still_plus():
    types = [token.type for token in tokenize("x + 1✨")]
    assert types[1] is TokenType.PLUS


def test_plus_equal_without_spaces():
    types = [token.type for token in tokenize("x+=1✨")]
    assert types[:3] == [TokenType.IDENTIFIER, TokenType.PLUS_EQUAL, TokenType.NUMBER]


def test_plus_equal_parses_as_assign():
    statement = only_statement("x += 1✨")
    assert isinstance(statement, Assign)
    assert statement.name.lexeme == "x"
    assert statement.operator.type is TokenType.PLUS_EQUAL
    assert isinstance(statement.value, Literal) and statement.value.value == 1


def test_plus_equal_value_is_full_expression():
    statement = only_statement("total += price * 2 + 1✨")
    assert isinstance(statement, Assign)
    assert statement.name.lexeme == "total"
    assert statement.operator.type is TokenType.PLUS_EQUAL
    assert isinstance(statement.value, Binary)


def test_plus_equal_value_can_reference_variables():
    statement = only_statement("count += other✨")
    assert isinstance(statement, Assign)
    assert isinstance(statement.value, Variable) and statement.value.name.lexeme == "other"


def test_plain_assign_still_uses_equal():
    statement = only_statement("x = 1✨")
    assert isinstance(statement, Assign)
    assert statement.operator.type is TokenType.EQUAL


def test_plus_equal_inside_block():
    (statement,) = parse_source("vibe ✅ { x += 1✨ }")
    assert isinstance(statement, If)
    (inner,) = statement.then_branch.statements
    assert isinstance(inner, Assign) and inner.operator.type is TokenType.PLUS_EQUAL


def test_plus_equal_inside_loop_body():
    statement = only_statement("ralph ❌ { n += 2✨ }")
    assert isinstance(statement, While)
    assert isinstance(statement.body, Block)
    (inner,) = statement.body.statements
    assert isinstance(inner, Assign) and inner.operator.type is TokenType.PLUS_EQUAL


def test_plus_equal_inside_clanker():
    statement = parse_source("clanker f() { x += 1✨ }")[0]
    (inner,) = statement.body.statements
    assert isinstance(inner, Assign) and inner.operator.type is TokenType.PLUS_EQUAL


def test_plus_equal_multiple_statements():
    statements = parse_source("x += 1✨\ny = x✨\nz += y✨")
    assert [type(s) for s in statements] == [Assign, Assign, Assign]
    assert [s.operator.type for s in statements] == [
        TokenType.PLUS_EQUAL,
        TokenType.EQUAL,
        TokenType.PLUS_EQUAL,
    ]


def test_ship_value_stops_before_plus_equal():
    with pytest.raises(SlopSyntaxError, match=r"expected ✨ after ship value, found '\+='"):
        parse_source("clanker f() { ship x += 1✨ }")


def test_plus_equal_missing_value_reports_expression():
    with pytest.raises(SlopSyntaxError, match=r"expected an expression, found '✨'"):
        parse_source("x += ✨")


def test_plus_equal_missing_value_at_end_of_file():
    with pytest.raises(SlopSyntaxError, match=r"expected an expression, but reached end of file"):
        parse_source("x +=")


def test_plus_equal_missing_terminator():
    with pytest.raises(SlopSyntaxError, match=r"expected ✨ after assignment, found '}'"):
        parse_source("clanker f() { x += 1 }")


def test_chained_plus_equal_is_rejected():
    with pytest.raises(SlopSyntaxError, match=r"expected ✨ after assignment, found '\+='"):
        parse_source("x += y += 1✨")


def test_space_between_plus_and_equal_is_not_compound():
    with pytest.raises(SlopSyntaxError, match=r"expected an expression, found '='"):
        parse_source("x + = 1✨")


def test_plus_equal_is_not_an_expression():
    with pytest.raises(SlopSyntaxError, match=r"expected '\)' after expression, found '\+='"):
        parse_source("1 + (x += 1)✨")


def test_ship_is_still_parsed_next_to_plus_equal():
    statements = parse_source("clanker f() { x += 1✨ ship x✨ }")
    body = statements[0].body.statements
    assert isinstance(body[0], Assign)
    assert isinstance(body[1], Ship)
