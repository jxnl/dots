---
name: gh-commit
description: "Review git changes and split them into semantic commits with clear messages. Use when the user asks to commit work, clean up local history, or group a mixed diff into logical commits. Do not commit on main or master unless the user explicitly asks."
---

# GH Commit

## Goal

Turn the current working tree into a small set of clean commits without mixing unrelated changes.

## Workflow

1. Verify git context.
- Run `git rev-parse --show-toplevel` and `git status -sb`.
- Read the branch with `git branch --show-current`.
- If the branch is `main` or `master`, stop and ask the user to switch/create a branch (recommend `codex/...`) unless they explicitly asked to commit on that branch.

2. Inspect all changes before staging anything.
- Run `git diff --stat` and `git diff --cached --stat`.
- List untracked files with `git ls-files --others --exclude-standard`.
- Read actual hunks with `git diff` and `git diff --cached`.
- Include untracked files in the review (read them if needed) so commit grouping decisions cover the full diff.

3. Propose semantic commit groups.
- Group by intent, not just file type (for example: bug fix, refactor, tests, docs).
- Keep user-authored unrelated work separate.
- Call out any files that need partial staging because they contain mixed concerns.

4. Create each commit group.
- Stage only the files or hunks for that group (`git add <paths>` or `git add -p`).
- Verify exactly what is staged with `git diff --cached --stat` and `git diff --cached`.
- Commit with a concise imperative message.
- Prefer `type(scope): summary` when the change has an obvious type/scope; otherwise use a clear plain-English summary.

5. Repeat until done.
- After each commit, re-check `git status -sb`.
- Continue until all intended changes are committed or intentionally left uncommitted.

6. Report the result.
- List the commit SHAs and messages in order.
- Note any remaining staged/unstaged/untracked files.

## Safety Rules

- Avoid `git add -A` unless the entire remaining diff belongs in one commit.
- Use partial staging when a file mixes multiple concerns.
- Do not rewrite or discard user changes unless explicitly asked.
- If grouping is ambiguous, ask before committing.
