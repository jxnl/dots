# Ship

Commit, push, and create PR in one step.

## Steps

1. Safety check
```bash
git branch --show-current
```
- If on `main`/`master`: stop and create a branch: `git checkout -b feat/short-desc`

2. Inspect changes
```bash
git status --porcelain
git diff --stat
```
- If no changes, stop

3. Stage + commit
```bash
git add path/to/file1 path/to/file2
git commit -m "type(scope): short description"
```
- Never `git add .`
- One commit unless changes are clearly separate concerns

4. Push
```bash
git push -u origin $(git branch --show-current)
```

5. Create PR if needed
```bash
gh pr view --json number 2>/dev/null
```
- If no PR: `gh pr create --title "type(scope): desc" --body "## Summary\n- changes"`
- If PR exists: report URL

Read if present: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`.
