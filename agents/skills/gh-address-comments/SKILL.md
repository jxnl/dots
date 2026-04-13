---
name: gh-address-comments
description: Help address review/issue comments on the open GitHub PR for the current branch using `oai_gh` or `gh`; verify auth first and prompt the user to authenticate if not logged in.
metadata:
  short-description: Address comments in a GitHub PR review
---

# PR Comment Handler

Guide to find the open PR for the current branch and address its comments with `oai_gh` when available, otherwise `gh`.

Prereq: ensure the GitHub CLI is installed and authenticated. Prefer `oai_gh auth status` when `oai_gh` exists on `PATH`, otherwise run `gh auth status`. If neither CLI is available or auth is missing, ask the user to install/authenticate before continuing.

## 1) Inspect comments needing attention
- Run scripts/fetch_comments.py which will print out all the comments and review threads on the PR

## 2) Ask the user for clarification
- Number all the review threads and comments and provide a short summary of what would be required to apply a fix for it
- Ask the user which numbered comments should be addressed

## 3) If user chooses comments
- Apply fixes for the selected comments

Notes:
- If GitHub auth/rate issues appear mid-run, prompt the user to re-authenticate with `oai_gh auth login` or `gh auth login`, then retry.
