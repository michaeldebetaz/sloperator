# AGENTS.md

This directory holds the recursive-descent parser for SlopLang. `docs/spec.md` defines the grammar. Keep `parser.py` consistent with it.

## Conventions

- **Use one method per grammar rule.** Each grammar production gets its own method on the parser class, named after the rule (for example `if_stmt`, `logic_or`, `call`). The method consumes exactly the tokens for that rule and calls other rule methods for its sub-rules. Do not fold several rules into one method or split one rule across several methods.

- **Make syntax errors describe what token was found.** Every `SlopSyntaxError` should say what was expected and which token was actually there, such as `expected ✨ after expression, found '}'`. Build errors through `error()` and `expect()` so the `found '...'` suffix stays consistent. At end of input, the message reports that the parser reached end of file instead of quoting a token.
