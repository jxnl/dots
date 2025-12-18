# Address PR Comments

Resolve actionable review comments for a PR, one-by-one.

## Steps

1. Checkout PR
```bash
gh pr checkout {PR}
```

2. Collect comments (review + issue comments)
```bash
gh pr view {PR} --json title -q .title
gh pr view {PR} --comments
```

3. Present a numbered list of actionable items (prefer file+line refs). Ask user which to handle.

4. For each selected item:
- Show relevant code context
- Make the smallest correct change
- Add/update tests when needed

5. Summary
```bash
git status --short
git diff --stat
```
