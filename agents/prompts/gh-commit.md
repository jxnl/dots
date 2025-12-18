# Commit

Create small, logical commits with conventional commit messages.

## Steps

1. Safety
```bash
git branch --show-current
```
- If on `main`/`master`: stop and create a branch: `git checkout -b feat/short-desc`

2. Inspect changes
```bash
git status --porcelain
git diff --stat
```

3. Batch changes (typical: `feat|fix`, then `test`, then `docs`, then `refactor/chore`)
- Keep commits atomic
- Do not mix unrelated concerns
- Never `git add .`

4. Stage + commit each batch
```bash
git add path/to/file1 path/to/file2
git commit -m "type(scope): short description"
```

5. Summary
```bash
git log --oneline -10
git diff --stat origin/$(git remote show origin | awk '/HEAD branch/ {print $NF}')...HEAD
```

Read if present: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `.gitmessage`.
