---
name: commit
description: Create a git commit after a Boot.dev lesson submitted with `bootdev run -s` passes all checks, using the message format "feat: finished CH<chapter>: L<lesson>: <title>"
---

# Commit

Use this skill only after `bootdev run -s <id>` has reported that the lesson passed. If the output shows any failed check, or the command errored, stop and report that. Do not commit.

## 1. Read the lesson from the output

The `bootdev run` output names the lesson on a line like `9.2 - Writing Skills`. Split it into:

- Chapter: the number before the dot (`9`)
- Lesson: the number after the dot (`2`)
- Title: the text after the dash (`Writing Skills`)

The commit message is:

```text
feat: finished CH<chapter>: L<lesson>: <title>
```

For the example above: `feat: finished CH9: L2: Writing Skills`

## 2. Review the changes

Run `git status` and `git diff` to see what the lesson changed. Stage only the files that belong to the lesson. Do not sweep in unrelated changes with `git add -A`. If you cannot tell which files belong to the lesson, ask before staging.

## 3. Commit

- Commit to the current branch. Do not create or switch branches.
- Do not push. Do not create a pull request.
- Do not amend or rewrite existing commits.
- Do not add a commit body or footer unless asked.

Run `git status` after committing and report the new commit hash and message.
