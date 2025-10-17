# De-Slop Command

Remove AI-generated artifacts before PR submission.

## Workflow

### 1. Context & Comparison

**Ask:** Compare against base branch or PR?
```bash
# If base branch
git diff --name-status $(git remote show origin | grep "HEAD branch" | cut -d ":" -f 2 | xargs)...HEAD

# If PR number provided
gh pr view {PR_NUMBER} --json baseRefName -q .baseRefName
git diff {BASE}...HEAD
```

### 2. Scan for Slop (Always Dry Run)

#### A. Unnecessary Markdown Files
Flag: NOTES.md, PLAN.md, ARCHITECTURE.md, THOUGHTS.md, IDEAS.md, SCRATCH.md, TEMP.md, TODO.md
Ignore: README.md, CONTRIBUTING.md, CHANGELOG.md, docs/**/*.md

#### B. Redundant Comments
```python
# Create user  ← Just restates next line
user = User()
```

#### C. AI TODOs
```python
# TODO: Add error handling
# TODO: Consider edge cases
```

#### D. Excessive Docstrings
Simple getter with 10-line docstring

#### E. Mock-Heavy Tests
```python
@patch @patch @patch  # >3 mocks, tests nothing real
```
Note: CLAUDE.md says "no mocking in tests"

#### F. Fake Data
Suspiciously specific metrics without citation, made-up case studies

### 3. Present Findings

```
🔍 Found X slop patterns

[1] NOTES.md (45 lines)
    → Delete: Unnecessary markdown

[2] src/user.py:23-28
    → Remove redundant comments:
    # Create user
    user = User()

[3] src/api.py:15-25
    → Simplify excessive docstring

[4] tests/test_user.py:50-70
    → Flag: Mock-heavy (5 mocks)

Enter numbers (1 2 4), range (1-4), 'all', or 'none':
```

### 4. Execute Selection

**File deletions:**
```bash
git rm {FILE}
```

**Code cleanup:** Use Edit tool, show before/after

**Flag-only items:** Show location, ask if open file

### 5. Summary

```
✅ Cleaned: 2 files deleted, 12 comments removed, 3 docstrings simplified
⚠️  Flagged: tests/test_user.py:50-70 (mock-heavy)

Next: Review flagged items, run tests, commit
```

## Detection Patterns

**Markdown files to flag:**
`NOTES|PLAN|ARCHITECTURE|THOUGHTS|IDEAS|SCRATCH|TEMP|TODO` (case-insensitive)

**Comment patterns:**
- Restates next line exactly
- `# TODO: (Add|Consider|Might|Should)`
- Emoji in code comments
- >3 line docstring for <5 line function

**Test patterns:**
- >3 `@patch` decorators per test
- No assertions on real behavior

**Fake data:**
- Specific percentages without source
- "According to studies" without citation

## Safety

- Always dry run first with numbered selection
- Never remove: README.md, CONTRIBUTING.md, CHANGELOG.md, docs/**
- When unsure: flag, don't delete
- Confirm if deleting >5 files or >50 lines

## Usage

```bash
/de-slop              # Compare against base
/de-slop 123          # Compare against PR #123
```

## Unresolved Questions

- Threshold for "excessive" docstring?
- Check commit messages for slop?
