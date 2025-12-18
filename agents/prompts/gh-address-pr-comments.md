# Address PR Comments Command

Interactive PR comment resolution workflow.

## Workflow

### 1. Fetch PR Data
```bash
# Get PR details and comments
gh pr view {PR_NUMBER} --json title,body,state,author,headRefName,baseRefName,url,reviews
gh api repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}/comments
gh api repos/{OWNER}/{REPO}/issues/{PR_NUMBER}/comments

# Checkout PR branch
gh pr checkout {PR_NUMBER}
```

### 2. Analyze Comments
- Filter actionable comments (exclude author, focus on file/line refs)
- Read affected files for context
- Categorize: CODE, STYLE, DOCS, TEST, QUESTIONS

### 3. Present Options
```
Found {N} comments to address on PR #{NUMBER}: {TITLE}

Actionable Items:
─────────────────────────────────────────────────────────

1. [CODE] {file_path}:{line_number}
   Reviewer: @{username}
   Comment: "{comment text}"
   Suggested change: {describe what needs to be done}

2. [STYLE] {file_path}:{line_number}
   Reviewer: @{username}
   Comment: "{comment text}"
   Suggested change: {describe what needs to be done}

─────────────────────────────────────────────────────────

Which items would you like me to address?
Options: "1,3,4" | "1-5" | "all" | "1"
```

### 4. Address Changes
For each selected item:
1. Show file context and explain the change
2. Apply the change with Edit tool
3. Report completion: `✓ Addressed item {N}: {description}`

### 5. Summary
```bash
git status --short
git diff --stat
```

Report changes made, remaining comments, and suggest next steps.

## Rules

**Prioritize**: File/line refs, directive language, maintainer feedback, unresolved discussions

**Skip**: Info-only comments, questions without suggestions, resolved/outdated, praise

**Safety**: No auto git ops, show before doing, preserve context

**Usage**: `/address-pr-comments 18` | `/address-pr-comments https://github.com/owner/repo/pull/123`

## Error Handling
- PR doesn't exist: Verify number/URL
- No comments: "No actionable comments found"
- Not authenticated: Prompt `gh auth login`
- Uncommitted changes: Warn user first
- File not found: Comment may be outdated
- Ambiguous comment: Ask for clarification
