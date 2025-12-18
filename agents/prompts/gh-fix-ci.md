# Fix CI

Find the first failing check, fix it, and re-run the smallest verification command.

## Steps

1. Identify failures
```bash
gh pr checks {PR} 2>/dev/null || true
gh run list --limit 10 2>/dev/null || true
```

2. Open logs (or paste the failure output). Focus on the root error.

3. Fix
- Prefer minimal, correct changes
- Do not “fix” by skipping tests

4. Verify locally (the narrowest command that covers the failure), then summarize:
- what failed
- what changed
- how to re-run
