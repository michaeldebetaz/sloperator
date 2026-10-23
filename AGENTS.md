# AGENTS.md

Sloperator is a tree-walking interpreter for SlopLang, written in Python 3.13 and managed with `uv`.

## Project layout

- `sloperator.py`: CLI entrypoint, delegating to `sloperator/runner.py`.
- `sloperator/lexer` → `sloperator/parser` → `sloperator/evaluator`: the interpreter pipeline.
- `tests/`: pytest suite. `test_examples.py` runs every file in `examples/`.
- `examples/`: runnable `.slop` programs. Each must exit 0, write nothing to stderr, and print something to stdout.
- `docs/spec.md`: SlopLang syntax and semantics.

## Validation

Run all four from the repo root before considering a change done:

1. `uv run pytest`
2. `uv run ruff format --check`
3. `uv run ruff check`
4. `uv run ty check`

## Regression tests

Add a regression test whenever you fix a bug or change language behavior. Put it in the existing `tests/test_<area>.py` that matches the change (for example, `test_lexer_regression.py` for lexer bugs). Use `uv run pytest -k name` to run a single test while iterating. Comparison regression tests live in `tests/test_comparisons.py`; run them with `uv run pytest tests/test_comparisons.py`.

## Language behavior

For SlopLang syntax and semantics, see [docs/spec.md](docs/spec.md). Check it before changing behavior.
