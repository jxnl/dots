# Review PR

Review a GitHub PR quickly but thoroughly, focusing on correctness, tests, and risk.

## Steps

1. Fetch basics + checks
```bash
gh pr view {PR} --json title,author,baseRefName,headRefName,additions,deletions,changedFiles -q .
gh pr checks {PR}
```

2. Check out and diff
```bash
gh pr checkout {PR}
BASE=$(gh pr view {PR} --json baseRefName -q .baseRefName)
git diff --stat "$BASE"...HEAD
git diff "$BASE"...HEAD
```

3. Review
- Summarize what changed and why
- Call out risky areas and missing tests
- Note style/maintainability issues only when they matter
- If PR is large: ask what to prioritize

4. Output
- Summary (purpose + risk)
- Must-fix items
- Should-fix items
- Any questions / follow-ups
