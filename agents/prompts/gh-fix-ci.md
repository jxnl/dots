# Fix CI

Auto-detect, analyze, fix CI/CD failures on any branch.

## Workflow

### 1. Detect Context
```bash
CURRENT_BRANCH=$(git branch --show-current)

# Main/master: use workflow runs
gh run list --branch "$CURRENT_BRANCH" --limit 5 --json databaseId,status,conclusion,name

# Feature branch: check for PR first, fall back to runs
gh pr status --json number,title,url,headRefName
```

**Priority:**
- PR provided: Use that
- Feature branch with PR: Use PR checks
- Feature branch without PR: Use `gh run list`
- Main/master: Use `gh run list`

### 2. Fetch Logs

**PR-based:**
```bash
gh pr view {PR} --json statusCheckRollup | jq '.statusCheckRollup[] | select(.conclusion == "FAILURE")'
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
gh api repos/${REPO}/actions/jobs/{JOB_ID}/logs > /tmp/ci-logs.txt
```

**Run-based:**
```bash
RUN_ID=$(gh run list --branch main --limit 5 --json databaseId,conclusion --jq '[.[] | select(.conclusion == "failure")][0].databaseId')
gh run view $RUN_ID --json jobs --jq '.jobs[] | select(.conclusion == "failure")'
gh api repos/${REPO}/actions/jobs/{JOB_ID}/logs > /tmp/ci-logs.txt
```

### 3. Parse Errors

**Common patterns:**
- Ruff: `Would reformat: {file}` → `uv run ruff format {file}`
- Tests: `FAILED tests/...`, `AssertionError`, `ModuleNotFoundError`
- Types: `error: Incompatible types`, `Missing return statement`
- Build: `SyntaxError`, `ImportError`

### 4. Fix & Report

For each issue:
1. Read affected files
2. Apply fix with Edit tool
3. Show diff
4. Report completion

```
✅ Fixed 3 issues:
  • Lint: app/api.py - Removed unused import
  • Test: tests/test_auth.py - Fixed assertion
  • Type: models/user.py - Added type hint

Next: /commit then git push
```

## Safety

**Main branch:** Warn, suggest hotfix branch
**Uncommitted changes:** Warn before proceeding
**Unclear fixes:** Flag for manual review
**Multiple failures:** Ask which to prioritize

## Usage

```bash
/gh-fix-ci              # Current branch
/gh-fix-ci 123          # PR number
/gh-fix-ci https://...  # PR URL
```
