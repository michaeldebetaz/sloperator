# Sloperator

A tree-walking interpreter for [SlopLang](docs/spec.md), written in Python.

```bash
uv run sloperator.py path/to/program.slop
uv run sloperator.py --check path/to/program.slop
```

`--check` reports syntax errors without running the file.

```bash
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

## Language

See [docs/spec.md](docs/spec.md) for the full SlopLang specification.

## Layout

- `sloperator.py`: command-line entrypoint
- `sloperator/`: lexer, parser, and evaluator
- `examples/`: sample programs
- `tests/`: pytest suite
- `playground/`: web editor for running programs. Start it with `uv run playground/server.py`, then open <http://localhost:8080>.
