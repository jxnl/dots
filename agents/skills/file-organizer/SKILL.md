---
name: file-organizer
description: Organize Jason Liu's Downloads and Desktop, rename vague files, move durable documents into ~/Documents, and mirror important documents to Google Drive after a safe plan is approved.
metadata:
  short-description: Organize Downloads, Desktop, Documents, and Drive
---

# File Organizer

Use this skill when Jason asks to organize, clean up, audit, rename, archive, or sync files from `~/Downloads` or `~/Desktop`, especially when documents should move into `~/Documents` or be mirrored to Google Drive.

## Core Rule

Default to **plan first, apply second**.

1. Inventory `~/Downloads` and `~/Desktop`.
2. Ignore system clutter like `.DS_Store`, `.localized`, and hidden metadata unless it is inside a moved folder.
3. Classify files and top-level folders.
4. Inspect file contents only when names or locations are vague.
5. Propose moves, renames, Google Drive syncs, and deletion-review candidates.
6. Apply changes only after explicit confirmation.
7. Write a Markdown cleanup log under `~/Downloads/.cleanup_logs`.

## Source And Destination Roots

- Sources: `/Users/jasonliu/Downloads`, `/Users/jasonliu/Desktop`
- Local permanent home: `/Users/jasonliu/Documents`
- Cleanup logs and state: `/Users/jasonliu/Downloads/.cleanup_logs`
- Code/project review: `/Users/jasonliu/dev/_incoming_review`
- Google Drive: mirror only after a local Drive root is discovered or Jason provides one.

## Required Reference

Before creating a cleanup plan, read `references/organization-rules.md`. It defines naming conventions, folder taxonomy, Desktop rules, sync policy, duplicate handling, and safety constraints.

## Safety Constraints

- Do not delete files by default. Put delete/trash candidates in the plan.
- Do not overwrite existing files.
- Compare destination conflicts when possible; keep both different files with a descriptive suffix.
- Leave intentional Desktop aliases and symlinks in place unless broken or clearly stale.
- Keep personal wire and bank details in Finance bank folders, never inside investment deal folders.
- If Google Drive is missing, complete the local plan and ask for the Drive path before syncing.

## Output Format

For plan-only runs, return a concise cleanup plan with:

- Summary of source folders inspected.
- Proposed moves and renames.
- Proposed `~/Documents` destinations.
- Proposed Google Drive mirror actions or the reason sync is blocked.
- Duplicate/delete-review candidates.
- Assumptions and items needing Jason's decision.

For approved apply runs, report:

- Actions applied.
- Actions skipped and why.
- Cleanup log path.
- Any unresolved items.
