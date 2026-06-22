# Skills Catalog

Codex skills stored for installation to `~/.codex/skills` via `./install.sh --skills` or `./install.sh --agents`.

Restart Codex after installing or updating skills so the frontmatter descriptions are reloaded.

## How To Use Skills

- Name a skill directly, such as `$audit-ai-code`, `$tweet-like-me`, or `use the Playwright skill`.
- Ask naturally with phrases from the skill description. The `description` field is the main recall surface, so include real trigger words there.
- Keep each skill narrow. Put detailed procedures in `SKILL.md`, and move long checklists or source material into `references/`.
- For personal-voice skills, use the named person's corpus. Do not reuse Jason Liu's email or tweet style for someone else; build a separate skill from that person's own sent email, Slack, or social examples with permission.

## Review And Cleanup

### `audit-ai-code`

Audit, de-slop, parameterize, modularize, or safely clean up AI-shaped backend/general code.

Use for Python, TypeScript, or general diffs with duplicate helpers, fixture hacks, hard-coded test data, over-defensive control flow, broad exception wrappers, config-bag or boolean-mode soup, hallucinated APIs, brittle tests, or local-idiom drift.

### `audit-ai-frontend`

Audit and repair AI-shaped frontend code, screenshots, and design diffs.

Use for React, Tailwind, shadcn/ui, HTML/CSS, dashboards, landing pages, or app screens that need component API review, parameterization, responsive/a11y fixes, design-system alignment, better copy, or less generic cards/gradients/fonts.

### `audit-ai-writing`

Audit pasted chatbot output, AI-cleanup diffs, docs, wiki drafts, Markdown/MDX, and source-backed articles for writing residue.

Use for generic AI fluff, weak audience model, inflated significance, vague attribution, leaked tokens, placeholders, broken markup, fabricated or mismatched citations, detector false positives, and practical rewrite guidance.

## Personal Voice And Drafting

### `email-like-me`

Draft, rewrite, critique, or learn from emails in Jason Liu's personal email voice.

Use for replies, follow-ups, intros, escalations, logistics, vendor/admin notes, investor/founder coordination, assistant delegation, and updates to the Jason-specific persona model.

### `tweet-like-me`

Draft, rewrite, critique, or reply on X/Twitter in Jason Liu's `@jxnlco` voice.

Use for tweets, replies, quote-tweets, Codex/product posts, feedback asks, launches, operator takes, and short social reactions.

## GitHub And Shipping

### `gh-address-comments`

Find and address review comments on the open GitHub PR for the current branch.

Use when the user asks to inspect unresolved PR comments, summarize review threads, implement selected fixes, or verify comment-related changes.

### `gh-commit`

Review a working tree and split changes into semantic commits.

Use for mixed diffs, commit cleanup, staging decisions, or writing clear commit messages without committing on `main`/`master` unless explicitly requested.

### `gh-fix-ci`

Inspect failing GitHub Actions checks and propose or implement approved fixes.

Use for failing PR checks, workflow logs, CI triage, test failures in Actions, and remote failure snippets.

### `yeet`

Stage, commit, push, and open a draft GitHub PR in one explicit flow.

Use only when the user asks for the full ship flow.

## Browser, Files, And Local Tools

### `simple-html-artifact`

Build or refine single-file, information-first HTML artifacts.

Use for static reports, explainers, briefs, dashboards, note indexes, research pages, and simple front ends where comprehension matters more than marketing.

## Codex Operations And Persistence

### `ultragoal`

Design, critique, set, create, activate, or run durable Codex goals.

Use for persistent or long-running objectives with verifiers, durable state, approval gates, completion proof, and bounded parent/child delegation.

### `loop`

Create and manage simple heartbeat automations attached to the current Codex thread.

Use when Jason invokes `$loop` or asks a thread to keep going, check again, follow up, retry, monitor, or resume on a recurring cadence.

### `self-improve`

Inspect Codex session history and propose improvements to behavior, skills, project `AGENTS.md`, or global Codex instructions.

Use for dream passes, repeated-correction mining, skill audits, and durable instruction proposals.

### `slidev-presentation-kit`

Create or edit Slidev presentations in Jason's presentations repo.

Use for new decks, existing slide edits, Slidev conventions, polishing, animation work, and repo-specific presentation references.

## Personal Ops

### `file-organizer`

Organize Downloads, Desktop, Documents, and Google Drive with safe plans.

Use for cleanup plans, vague filename review, duplicate/delete candidates, approved moves/renames, Drive mirroring, and cleanup logs.
