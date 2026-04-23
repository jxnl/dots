---
name: simple-html-artifact
description: Build or refine single-file information-first HTML artifacts, especially index.html or text.html pages, with strong information hierarchy, restrained styling, accessible semantics, and minimal AI-generated frontend tells. Use when creating static HTML reports, research pages, explainers, briefs, dashboards, note indexes, or simple front ends whose goal is comprehension rather than marketing conversion.
---

# Simple HTML Artifact

Use this for static, single-page HTML artifacts that explain, compare, summarize, or organize information. Default to one browser-openable `index.html` or `text.html` file with Tailwind CDN. Add JavaScript only for filtering, sorting, copying, disclosure, or keyboard-safe interaction.

## Goal

Optimize for comprehension, orientation, retrieval, and trust, not conversion. The first viewport must show real information, not only hero copy.

Default priorities:
- Reading path: summary -> evidence -> reference.
- Claims paired with definitions, caveats, dates, assumptions, or sources when needed.
- Semantic HTML, readable type, mobile fit, keyboard order, print readability, and contrast.
- One subject-specific retrieval device: decision path, annotated scale, timeline rail, message template, field-guide strip, map, checklist, or compact diagram.

Avoid:
- Generic AI SaaS: gradient hero, glass cards, icon grids, abstract glows, repeated rounded cards, vague CTAs.
- Civic-document drift: beige/off-white page wash, low-contrast gray text, boxed nav chips, heavy dividers, bordered panels everywhere.
- Subject cliche drift: coffee pages do not need to be brown, wine pages do not need to be burgundy, finance pages do not need to be blue. Use motif color as an accent unless the user asked for a themed page.
- Fake completeness: made-up metrics, arbitrary percentages, placeholder data, decorative charts, or visuals implying false precision.

## Brief

Before styling, decide:

```text
Subject:
Audience/context:
Reader job:
Posture:
Primary surface:
Type direction:
Color direction:
Deviation reason, if any:
```

Carry forward explicit user preferences: information-first pages, no generic AI aesthetics, no line-heavy civic layouts, Tailwind by default, and `bg-white` by default.

If editing an existing artifact, inspect it first and preserve its copy, IA, density, tokens, and primitives unless they are the defect.

Use web search only when the subject is broad, current, culturally specific, or visually ambiguous. Look for comparable information artifacts, not marketing pages. Extract design logic: type role, density, color relationship, diagram language, label style, and the surface that carries the information.

Choose a posture that constrains taste, such as editorial guide, field guide, research brief, technical reference, museum label, workshop handout, or operating checklist. No posture usually means generic SaaS or government-document drift.

## Information Architecture

Start with the reader job:
- **Orient**: purpose, audience, scope, main question.
- **Decide**: 3-5 key claims, rules, risks, rankings, or recommendations.
- **Inspect**: examples, excerpts, visuals, rows, scales, notes, or tables.
- **Retrieve**: anchors, labels, section names, compact references.

Default order: title and purpose, useful metadata, concrete key points, one primary surface, supporting sections by reader need, caveats/method/sources near the relevant claims or near the end.

For one-pagers, compose one artifact rather than reusable app sections. Add sticky nav, rails, or repeated section chrome only when page length requires navigation.

Use a digestibility ladder:
- First screen: title, one useful rule or takeaway, and the beginning of the primary surface. Keep the H1 to 1-2 lines on desktop and start the primary surface before the first viewport is half over.
- Middle: the working reference, with labels/rows/checklists doing most of the work.
- End: examples, caveats, source notes, templates, or print/share material.
- Each section should have one job: decide, compare, explain, retrieve, or copy.

Headers must be one-column by default: eyebrow, H1, one-sentence purpose, then optional compact rule/metadata below in the same flow. Do not use a header grid/flex split, summary card, metric strip, or side panel beside the H1 unless the user provides a real paired relationship.

## Surface Choice

Do not default to tables, matrices, dashboards, or two columns. Pick by reader action:
- Compare identical attributes -> table or matrix.
- Choose among options -> decision tree, ranked strips, "choose this if", scorecard.
- Learn a taxonomy -> field-guide entries, specimen cards, annotated map, glossary.
- Understand sequence -> timeline, process diagram, checklist, flow.
- See relationships -> axis map, cluster diagram, annotated scale, small multiples.
- Remember rules -> rule cards, do/avoid pairs, recipe, cheat sheet.
- Monitor state -> compact dashboard with definitions.

Use tables only when rows share attributes and column scanning beats prose. Use two columns only for paired relationships: overview/detail, map/list, before/after, controls/results, image/annotation, or claim/evidence. Use SVG only when it explains, locates, compares, encodes scale, or gives subject-specific identity.

After the primary surface, choose 1-2 different retrieval shapes. Do not turn every section into another table, card grid, or equal-width column set.

## Visual Defaults

Keep the layout as narrow as the content allows: prose usually fits `max-w-3xl` to `max-w-4xl`; wide surfaces can use `max-w-5xl` to `max-w-6xl`. Keep prose around 65-80 characters per line. Use stable dimensions for fixed grids, charts, and controls.

Use type, alignment, whitespace, tint, and composition before borders. Leave some modules unboxed. If most sections need lines, the hierarchy is flat.

Default to `bg-white`. Use off-white, tinted, dark, or textured backgrounds only for user preference, brand/source palette, subject motif, print requirement, or hierarchy. Use Tailwind stock colors: dark text, muted text, light line, one accent scale, at most one supporting tint. Every added hue needs a job: category, sequence, status, warning, selected state, or cited subject cue. If the hue can be swapped without changing comprehension, remove it.

Choose type by posture. Keep four roles at most: display, section heading, body, caption/label. Pair fonts by role contrast, not novelty. If loading external fonts, use at most two families and `font-display: swap`; otherwise use system `serif`, `sans`, and `mono` intentionally.

Avoid policy-manual drift: no more than one typographic layer uses letterspacing or all-caps labels; borders should separate different information types, not decorate every box.

## Content Discipline

Set length by job: summaries use 3-5 concrete claims; table cells stay compact; diagram labels explain position or relationship; prose keeps one idea per paragraph; caveats and sources stay near claims they change.

If a section is too long, convert prose into labels, rows, scales, captions, or do/avoid pairs. If too thin, add an example, comparison, caveat, definition, or decision rule. Do not add generic overview paragraphs to make the page feel complete.

For quick-reference artifacts, design around the reader's next decision, not complete coverage. Use 4-6 major sections and one to two desktop screens. After the primary surface, add at most two supporting sections: one explanation/shortcut surface and one caveat/template/check surface. If it grows longer, cut examples, definitions, and source prose before adding navigation.

Mark assumptions, dates, freshness, scope, confidence, sources, and placeholder data when they affect interpretation. Keep source/freshness notes compact: a strip, caption, or short footer unless the user asks for a source section. Do not turn safety-sensitive topics into compliance reports. Do not invent metrics, ratings, examples, or benchmarks to fill a layout. Charts/SVGs need units, labels or legend, and a takeaway caption.

## Tailwind Defaults

Use Tailwind CDN: `<script src="https://cdn.tailwindcss.com"></script>`. Use Tailwind classes for layout/color/type/spacing/states. Use `<style>` only for print styles, details Tailwind cannot express cleanly, or fully offline artifacts. Do not add build tooling, frameworks, npm installs, or generic helper classes unless repetition justifies them.

Avoid template tells: `rounded-2xl shadow-xl bg-white p-6`, purple-blue gradients, frosted panels, large icon badges, boxed nav chips, and repeated horizontal rules. `border`, `divide-*`, and `ring-*` should separate different information types or interactive states. Arbitrary colors need a reason.

## Final Check

Before finishing:
1. Remove fake data, arbitrary percentages, placeholders, lorem ipsum, and conversion copy unless requested.
2. Remove repeated section shells, equal-weight panels, decorative SVGs, excessive comments, and JavaScript that native HTML can handle.
3. Pick the 2-3 weakest things and improve those first: usually hierarchy, verbosity, surface choice, or visual sameness.
4. Check keyboard/focus, labels, contrast, touch targets, mobile overflow, long text, print/readability, and semantic HTML.
5. If it still feels generated, fix structure and copy before changing colors, shadows, or fonts.
