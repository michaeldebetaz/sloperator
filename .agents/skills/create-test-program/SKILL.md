---
name: create-test-program
description: Given a SlopLang language feature, write an example program in examples/ and an exact-output test for it in tests/test_example_outputs.py
---

# Create Test Program

Input: a language feature (for example, "while loops", "string escapes", "unary minus"). If the feature is ambiguous or not in the spec, ask before writing anything.

## 1. Read the spec

Read `docs/spec.md` and find every section that defines the feature: its syntax, its semantics, and any error cases. The spec is the source of truth. Do not infer behavior from the interpreter's current output.

## 2. Write the example

Create `examples/<feature>.slop` using a lowercase snake_case name that does not already exist in `examples/`.

- Use only syntax the spec defines. Use smart quotes (`“ ”`), `✨` terminators, and `—` comments.
- Exercise the feature directly. Keep the program small and deterministic.
- Print results with `hallucinate(...)✨` so the output is observable.
- Include a brief `—` comment at the top naming the feature, matching `strings.slop`.
- Do not write error-case programs here. Examples must exit 0 and write nothing to stderr.

## 3. Derive the expected output by hand

Work out the exact stdout from the spec, line by line. Booleans print as `✅`/`❌`, nil as `nil`, strings without quotes, and each `hallucinate` call ends with a newline.

Then run the program to confirm:

```bash
uv run sloperator.py examples/<feature>.slop
```

If the output differs from your hand-derived value:

- If the spec says your expectation is right, the interpreter has a bug. Report it and stop. Do not change the expected value to match.
- If your reading of the spec was wrong, fix your expectation and say so.

## 4. Add the exact-output test

Open `tests/test_example_outputs.py`. If it does not exist, create it with this structure:

```python
"""Exact stdout for example programs that exercise specific language features."""

from pathlib import Path

import pytest

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"

CASES = {
    "hello.slop": "Hello, world!\n",
}


@pytest.mark.parametrize("name", CASES)
def test_example_output(name: str):
    result = run_source((EXAMPLES / name).read_text(encoding="utf-8"))
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == CASES[name]
```

If the file already exists, add a new entry to `CASES` and keep the existing structure. Use the file name as the key and the full expected stdout as the value, with `\n` escapes written explicitly so the expected output is visible.

Do not stage or commit the changes.
