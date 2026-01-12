---
name: slidev-presentation-kit
description: "Create or edit Slidev presentations in the /Users/jasonliu/dev/presentations repo. Use for drafting new decks, editing existing slides, applying repo-specific Slidev conventions, and polishing/animation work. Triggers: Slidev slide requests, layout/components usage, deck setup, or presentation workflow guidance for this repo."
---

# Slidev Presentation Kit

## Overview

Create and modify Slidev decks in `slides/decks/` using the repo's drafting and polishing workflow. Ask only when blocked, work incrementally, and change one slide at a time.

## Workflow Decision Tree

- **New presentation or heavy drafting**: Read `references/repo/docs/DRAFTING.md` then `references/repo/docs/BASICS.md`. Avoid animations.
- **Editing existing slides**: Read `references/repo/AGENTS.md` for workflow rules, then `references/repo/SLIDEV.md` for conventions.
- **Polishing or animations**: Read `references/repo/docs/POLISHING.md` and `references/repo/SLIDEV_POLISHING.md` before making changes.
- **Syntax lookup**: Check `references/repo/docs/REFERENCE.md` first, then `references/repo/docs/ADVANCED.md` if needed.
- **Components**: Use only QRCode during drafting; full component set only during polishing. See `references/repo/slides/components/README.md`.

## Core Rules

- Ask clarifying questions only when a decision is truly blocking; otherwise assume and proceed.
- Make one change at a time and get feedback before continuing.
- Work on one slide at a time; do not batch edits.
- Do not add animations during drafting.
- Keep click alignment comments and speaker notes synchronized when using `v-click`.

## Repo Setup

- Each deck needs a `components/` symlink to `../../components`. See `references/repo/AGENTS.md` for the exact command.
- Always check for deck-specific `slides/decks/<deck-name>/AGENTS.md` in the repo before editing a deck.

## References

Use `references/repo/` as the primary source of truth for this repo. It mirrors all Markdown in `/Users/jasonliu/dev/presentations` except `slides/decks/`.

Key entry points:

- `references/repo/AGENTS.md`
- `references/repo/SLIDEV.md`
- `references/repo/SLIDEV_POLISHING.md`
- `references/repo/docs/`
- `references/repo/slides/README.md`
- `references/repo/slides/components/README.md`
