---
name: audit-ai-frontend
description: Audit AI-generated, AI-shaped, or AI-looking frontend code, UI screenshots, and design diffs. Use for prompts like "audit AI frontend", "de-slop UI", "componentize this screen", "parameterize this React/Tailwind/shadcn UI", "make it responsive/accessible", or "review design-system drift"; check component APIs, reusable props/data models, modular composition, shared primitives/tokens, responsive resilience, accessibility, copy quality, hard-coded fixture screens, one-off CSS piles, and generic cards/gradients/fonts.
---

# AI Frontend Audit

## Use

Audit or repair frontend UI/code that looks generically AI-generated, while preserving existing product structure unless the user asks for a redesign.

Review in this order:

1. Establish the local contract.
   - Read components, routes/pages, CSS/theme tokens, existing primitives, design-system conventions, copy style, and data/state patterns.
   - If runnable, inspect the UI in a real browser with whatever browser tooling is available; this skill decides what to inspect, not browser mechanics.
   - If screenshot-only, review visuals but label implementation risks as `Inferred`.

2. Inspect data flow and component shape before styling.
   - Check whether repeated UI is parameterized through props/data or hard-coded as a fixture screen.
   - Look for reusable primitives, narrow component APIs, stable variants, shared state/data models, and realistic loading/empty/error/long-content cases.
   - Flag duplicated JSX, one-off CSS piles, brittle utility strings, boolean-mode soup, over-broad components, and visual constants that should be tokens.

3. Load only the reference you need.
   - `references/patterns.md` for concrete AI-tell and code-smell fixes.
   - `references/rubric.md` for broad UX/a11y/component/design audits.
   - `references/workflows.md` for code-structure, browser QA, reference-packet, and brief-lock loops.

4. Preserve local system intent while removing accidental defaults.
   - Keep copy/order/IA and known product tokens unless the user asks for a redesign.
   - Keep a common-looking font/card/palette only if adjacent screens or documented tokens already use it; replace it when the style exists only in the generated screen.
   - If references are missing, derive one explicit design contract from product domain + user job + existing primitives; do not fabricate named reference sites.

5. Fix in this order.
   - `P0`: keyboard, labels, contrast, touch targets, mobile overflow, missing loading/empty/error states.
   - `P1`: hard-coded fixture screens, weak data models, duplicated markup/styles, brittle component APIs, token drift, boolean-mode soup.
   - `P1`: generic SaaS layout, card overuse, icon-pill repetition, Inter/Roboto/system defaults, purple/indigo/cyan gradient/glass tropes, vague CTA/copy.
   - `P2`: spacing rhythm, token consistency, one memorable visual rule, reduced-motion and state polish.

6. Re-verify in browser after edits whenever possible.

## Output

For each finding, include:

- `Issue`
- `Evidence`
- `Class` (`P0`, `P1`, `P2`)
- `Root cause` (`Component/API`, `Data/state`, `Responsive/a11y`, `Design-system`, `Copy`, `Visual default`)
- `Why it matters / why it reads as generic`
- `Possible non-AI explanation`
- `Smallest fix`
- `Acceptance check`
- `Confidence` (`High`, `Medium`, `Low`)
- `File/line` when code is available

Return only the top 5-8 findings and merge repeated symptoms under one root cause. End with one line: `If I had to change only one thing: ...`

For implementation asks, patch the code directly. Prefer the smallest local abstraction that makes the next screen/state easier: typed data, props, variants, slots/children, existing primitives, or tokens. Summarize only meaningful component/design changes and remaining risk.

## Guardrails

- Treat "AI-looking" as a quality smell, not a provenance claim.
- Prefer objective defects over taste opinions.
- Prefer local idiom over a new abstraction. Componentize only when it removes duplication, supports real states/data, or matches established primitives.
- When auditing shadcn/ui projects, preserve semantic component usage and tokens. Use the `shadcn` skill if component APIs, registry install/update, or shadcn-specific composition rules are part of the fix.
- Avoid anti-slop overcorrection: no random ornaments, novelty fonts, or one-off visual chaos.
- Anchor each finding in code, screenshots, DOM/a11y snapshots, or browser behavior, and separate fact from inference.

## Resource

- `references/patterns.md`: checklist of AI-frontend tells, code smells, and repair patterns.
- `references/rubric.md`: compact UX/a11y/component/design-quality rubric for broader audits.
- `references/workflows.md`: code-structure audit, browser QA, reference-packet, and brief-lock loops.
- `references/sources.md`: research basis and links for periodic prompt refreshes.
