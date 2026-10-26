---
description: Commit after a Boot.dev lesson passes `bootdev run -s`, using the message "feat: finished CH<chapter>: L<lesson>: <title>"
---

# Commit lesson

Use this command only after `bootdev run -s <id>` has reported that the lesson passed. If the `bootdev run` output is not in this conversation, stop and ask for it. If the output shows any failed check, or the command errored, stop and report that. Do not commit.

Lesson ID, if provided: $ARGUMENTS

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

Run `git status` to see every uncommitted file. Stage all of them with `git add -A` so the lesson lands in a single commit. Do not split changes into separate commits.

## 3. Commit

- Commit to the current branch. Do not create or switch branches.
- Do not push. Do not create a pull request.
- Do not amend or rewrite existing commits.
- Do not add a commit body or footer unless asked.

Run `git status` after committing and report the new commit hash and message.
