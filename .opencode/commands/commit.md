---
description: Review the diff, commit all project changes with a message, and rebase onto origin/main
---

Commit the project changes with the message: $ARGUMENTS

1. Run `git status` and `git diff` (plus `git diff --staged`) to review every pending change. Look for bugs, leftover debug code, secrets, and unrelated edits. If something looks wrong, stop and report it instead of committing.
2. If $ARGUMENTS is empty, stop and ask for a commit message.
3. Stage the project changes with `git add -A`.
4. Commit with the message `$ARGUMENTS`. Keep it a short, single-sentence conventional commit message.
5. Run `git pull --rebase origin main`. If there are conflicts, stop and report them.
6. Show the result with `git log --oneline -5` and `git status`.
