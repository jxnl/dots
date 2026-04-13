---
name: audit-ai-writing
description: Reference-only checklist for AI-writing artifacts, citation failures, and cleanup rewrites in Markdown, MDX, wiki text, or pasted chatbot output. Use when you need objective residue checks, false-positive-safe prose triage, and practical fixes without relying on detector scores.
---

# AI Writing Audit

## Use

Audit or repair Markdown, docs, and pasted prose that may contain AI-writing residue, broken citations, or house-style drift.

Open `patterns.md` and review in this order:

1. Machine residue, broken markup, and broken citations.
2. Citation-claim mismatches, vague attribution, and unsupported claims.
3. Repetitive style patterns and house-style drift.
4. Rewrite to concrete facts, plain source-backed attribution, and target-format markup.

## Output

For each finding, include:

- `Issue`
- `Evidence` (exact snippet or line location)
- `Class` (`P0`, `P1`, `P2`)
- `Why it matters / why it reads as generated`
- `Possible non-AI explanation`
- `Smallest fix`
- `Acceptance check`
- `Confidence` (`High`, `Medium`, `Low`)
- `File/line` when a file is available

Return only the top 5-8 findings and merge repeated symptoms under one root cause. For rewrite asks, patch the text directly and summarize only the meaningful cleanup.

## Guardrails

- Do not claim AI authorship from a single style cue, detector score, perfect grammar, or formal/multilingual English.
- Prefer objective residue and source verification before provenance speculation.
- Treat suspicious markers as text-quality defects first, not proof of authorship.
- Use this checklist for review and rewrite guidance. Only patch files if the user asks for edits.

## Resource

- `patterns.md`: compact artifact taxonomy, verification checks, rewrite guidance, and source basis.
