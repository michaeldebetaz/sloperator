# AGENTS.md

Sloperator is a tree-walking interpreter for SlopLang, written in Python 3.13 and managed with `uv`. It has no runtime dependencies; dev tools are pytest, ruff, and ty.

## Commands

- Run a program: `uv run sloperator.py path/to/file.slop`. Add `--check` to report syntax errors without running.
- Full validation, from the repo root: `uv run pytest`, then `uv run ruff format --check`, `uv run ruff check`, `uv run ty check`. The `validate` skill (`.agents/skills/validate`) omits `ty check`; run it anyway.
- Single test: `uv run pytest tests/test_evaluator.py::test_name` or `uv run pytest -k name`.
- Ruff uses line length 100 and rules E, F, I, UP, B.

## Layout

- `sloperator.py`: CLI entrypoint. It calls `sloperator/runner.py` (`run_program`, `check_program`, and `run_source`, which tests use).
- Pipeline: `sloperator/lexer` (`tokenize`) → `sloperator/parser` (`parse`) → `sloperator/evaluator` (`Interpreter`).
- `docs/spec.md` is the source of truth for SlopLang syntax and semantics. Check it before changing language behavior.
- `examples/*.slop`: `tests/test_examples.py` runs every file and requires exit 0, empty stderr, and non-empty stdout. Any new example must satisfy this.
- `playground/server.py`: web UI at `http://localhost:8080` (`uv run playground/server.py [port]`). It runs each program in a subprocess with a 5 s timeout and appends every run to `logs/runs.log`, which is gitignored.
- `.opencode/plugins/run-slop.ts` registers a `run_slop` tool that wraps `uv run sloperator.py`.

## SlopLang gotchas

- Source uses non-ASCII tokens. Write them exactly. Straight `"` is a lexical error.
  - Strings use `“ ”` (U+201C/U+201D).
  - Statements end with `✨` (U+2728). It is required and never follows a closing brace.
  - Comments start with `—` (U+2014).
  - Booleans are `✅` and `❌`.
- Keywords: `slop` (mutable var), `loadbearing` (const), `clanker` (fn), `vibe`/`nah` (if/else), `ralph` (while), `hallucinate` (print), `ship` (return). There is no `break`, `continue`, `for`, or `else if`.
- Conditions must be booleans. There is no truthiness. Functions must be declared before they are first called. Calls must match arity exactly.
- Call depth is capped at 500 and reports a `stack overflow` runtime error. Runtime errors go to stderr, not as Python tracebacks. Any traceback is a bug.

## Environment

- `.ignore` hides `uv.lock` from ripgrep-based search. Read it directly if you need it.
- `opencode.jsonc` denies reads of `*.env`. Do not try to read `.env`.
