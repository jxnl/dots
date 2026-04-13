---
name: audit-ai-frontend
description: Audit AI-generated or AI-looking frontend implementations, UI screenshots, and design diffs for generic AI aesthetics, card/gradient/font tells, weak UX copy, accessibility gaps, brittle responsive behavior, and one-off design-system drift. Use when reviewing or restyling React, Tailwind, shadcn/ui, HTML/CSS, landing pages, dashboards, or app screens to make the UI feel more intentional without a full redesign unless explicitly requested.
---

# AI Frontend Audit

Use this one-page scale to audit or repair frontend UI that looks generically AI-generated. Treat model/tool clues as weak priors; judge the shipped experience.

## Scale

`S0` Blockers: broken keyboard, labels, focus, contrast, touch targets, mobile layout, or missing loading/empty/error states.

`S1` Product truth: fake metrics, demo data, missing source/date labels, UI/API/schema drift, auth or tenancy assumptions, no retry or recovery.

`S2` Local fit: ignores the repo's component library, tokens, typography, density, adjacent screens, or established interaction states.

`S3` Task hierarchy: generic dashboard or landing-page structure, all panels equal weight, unclear primary action, weak IA.

`S4` AI aesthetic defaults: Inter/system-only personality, purple/indigo/cyan gradients, glass/glow layers, rounded-card grids, Lucide icon pills, vague CTA/copy, overlong explanatory prose, repeated section shells.

`S5` Tool fingerprints: v0/shadcn registry shells, Claude artifact polish, Codex minimal-diff conservatism, Gemini explainer layouts, Lovable/Supabase app shells, Bolt/Replit fallback scaffolds, Figma layer residue.

`S6` Creative polish: fun styles, algorithmic art, theme packs, image assets, stickers, motion, or novelty that does not affect the core task.

## Do

- Inspect code and UI together before proposing changes.
- Rank findings by the scale above; fix lower-numbered issues before style.
- Preserve local copy, IA, tokens, and component primitives unless they are the problem.
- Use installed icon packs or existing icon components by default; custom SVGs are only for bespoke product marks, diagrams, or assets the icon set cannot express.
- Use source/tool clues only to expand searches, for example `CardHeader`, `text-muted-foreground`, `lucide-react`, `supabase`, `VITE_`, fixed `left/top/width/height`, `features.map`, `bg-clip-text`.
- Replace generic polish with product-specific hierarchy: one primary action, one dominant data surface, concrete object/action copy, and realistic states.
- When a UI still feels AI-generated after visual cleanup, cut copy and change the information structure before changing colors or adding decoration.
- Verify runnable UIs in browser at desktop and mobile sizes, including keyboard/focus, long text, empty data, loading, errors, disabled states, and reduced motion.

## Don't

- Don't claim AI authorship from style, model fingerprints, or component choices.
- Don't prioritize fun skills, stickers, algorithmic art, theme packs, or dramatic motion above operability and product truth.
- Don't overcorrect generic UI with random ornaments, novelty fonts, noisy textures, or one-off visual chaos.
- Don't keep repeated card grids, bordered panels, or long prose blocks just because they are already implemented; collapse them into rows, matrices, labels, or plain text when the content is simple.
- Don't hand-roll inline SVG icons when the repo already has `lucide-react`, Heroicons, Font Awesome, Radix icons, Material icons, or another installed icon system.
- Don't replace a documented design system just because it uses common fonts, cards, or neutral tokens.
- Don't report inferred accessibility or code defects from screenshots as fact; mark them `Inferred`.
- Don't leave pretty demo states in place of real authorization, validation, empty, error, setup, or API contract behavior.

## Output

For review-only asks, return the top 5-8 findings with `Issue`, `Evidence`, `Scale`, `Class`, `Smallest fix`, `Acceptance check`, `Confidence`, and `File/line`. Merge repeated symptoms under one root cause and end with `If I had to change only one thing: ...`

For implementation asks, patch directly, then summarize the meaningful design changes and remaining risk.

Use `references/patterns.md`, `references/rubric.md`, `references/workflows.md`, and `references/sources.md` only when the one-page scale is not enough.
