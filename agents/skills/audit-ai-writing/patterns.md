# AI Writing Patterns and Fixes

Compact checklist for AI-writing residue, citation failures, and cleanup rewrites. Adapted from Wikipedia's "Signs of AI writing" and reinforced with writing-style and citation-integrity research. This is a review guide, not proof of authorship.

## Review order

1. Fix machine residue, malformed markup, and citation failures.
2. Verify every suspicious claim against the cited source text, not just the link or DOI.
3. Rewrite vague or overconfident prose into concrete, dated, source-backed statements.
4. Check quotes, numbers, dates, and causal language for source drift.
5. Treat style cues as weak signals only after genre/context checks, then normalize to house style.
6. Re-scan for placeholders, unsupported superlatives, and stale speculation.

## Rule: remove machine residue and format/schema hallucinations

Machine residue:

- Leaked tool/citation tokens: `turn0search0`, `turn0image0`, `turn0news0`, `turn0file0`, `oaicite`, `oai_citation`, `contentReference[...]`, `attributableIndex`, `generated-reference-identifier`, `[attached_file:1]`, `[web:1]`, `grok_card`, `grok-card`, stray `+1`.
- Private-use citation glyphs rendered as odd symbols, including wrapped `\ue200...\ue202` markers.
- Placeholder values: `INSERT_SOURCE_URL`, `URL_HERE`, `PASTE_*_URL_HERE`, `2025-XX-XX`, bracketed drafting instructions.
- AI copy/paste leftovers: `As an AI language model...`, `I hope this helps`, `Would you like me to...`, `Sure, here...`, `Certainly...`, `Below is...`, "copy and paste this", orphaned `Subject:`, orphaned `Draft:` / `Response:`.
- Tracking params from copied chatbot links: `utm_source=chatgpt.com`, `utm_source=openai`, `utm_source=copilot.com`, `referrer=grok.com`.

Format/schema hallucinations:

- Wrong markup for the destination format: Markdown headings/bold/links in MediaWiki text, fenced code wrappers around prose, skipped heading levels, duplicate anchors.
- Invalid or hallucinated wiki structures: non-existent templates/categories, pre-placed maintenance templates, AfC "submission statement" residue, unused named references dumped into a references section.
- Broken Markdown references: undefined reference labels, unused reference definitions, empty links, invalid fragment IDs.
- Broken internal references: links to headings/files that do not exist, invented section names, or "see above/below" pointers that no longer match the document structure.

Citation integrity failures:

- Nonexistent source, fake article/chapter title, or real venue/publisher with invented metadata.
- Valid DOI/PMID/ISBN that resolves to a different work than the citation text.
- Link text and hyperlink target point to different works.
- In-text citation has no bibliography entry, or bibliography entries are never cited in the body.
- Book or chapter citation lacks page numbers for a specific claim.
- Quoted text, speaker names, or publication dates do not match the cited source.
- Round statistics or precise percentages appear without a source that actually states that number.

Fix:

- Delete residue and placeholder text. Replace with verified citations or remove the claim.
- Convert markup to the target format and run deterministic link/render checks if available.
- For high-impact claims, confirm author/title/date/venue plus claim support in 2-3 authoritative sources before keeping the text.
- Do not label a reference "hallucinated" until you rule out a dead link, archive drift, or a minor citation typo.

## Rule: rewrite unsupported prose, vague attribution, and template structure

- Generic scene-setting intros: "In today's fast-paced world...", "In an era where...", "This article explores...", "Let's dive in...".
- Generic significance language: "marked a pivotal moment", "underscores its significance", "enduring legacy", "broader landscape", rhetorical `serves as` / `stands as`.
- Weasel attribution: "experts argue", "observers note", "some critics say", "several publications", "independent coverage" as body prose.
- Knowledge-gap boilerplate and speculation: "As of my last knowledge update", "Based on available information", "Specific details are limited", "likely supports", "keeps a low profile".
- Formula sections with weak sourcing: "Despite these challenges...", "Future Outlook", generic conclusions that restate themes without new evidence.
- Overstated or unverifiable claims: "best", "fastest", "revolutionary", "guarantees", broad security or performance assertions with no cited data.
- Citation drift: source exists, but author/title/date was silently normalized, paraphrased, or rounded enough that retrieval or attribution becomes wrong.
- Over-balanced filler: "on one hand / on the other hand", "while there are many factors", or broad caveats that avoid making a checkable claim.
- Causal overreach: "led to", "drove", "enabled", "therefore", "as a result" when the source only supports sequence, correlation, or opinion.
- Softened unsourced quantification: "many", "numerous", "a wide range of", "substantial", "significant" with no count, timeframe, or denominator.

Fix:

- Replace abstract praise with who/what/when/where and the exact source that supports the claim.
- Name the source or remove the attribution. Do not imply consensus from one weak source.
- Cut speculation and state only what is verified. Use absolute dates or versioned scope when timing matters.
- Fold real constraints into topical sections and delete empty "future/challenges" filler.
- Delete generic intro/outro scaffolding and start with the concrete subject, claim, and evidence.
- Downgrade causal verbs to neutral chronology unless a source explicitly supports causation.
- Replace vague volume claims with exact counts, dates, and denominators, or remove them.
- Write one idea per sentence where possible, put the actor near the front, define jargon once, and avoid "please note", "at this time", "simply", and "quickly" filler.

## Rule: verify quotes, numbers, names, and dates exactly

- Quotes that sound polished but do not match the source text verbatim, or quote punctuation/ellipsis that changes meaning.
- Speaker/title drift: person names, company names, venue names, paper titles, and API or product names are close but not exact.
- Number drift: rounded metrics, percentages, rankings, and date ranges copied into bullets or tables but not stated that way in the source.
- Vague time anchors in durable docs: "recently", "currently", "today", "now", "in recent years", "soon".
- Unsupported roadmap language: "planned", "upcoming", "will support", "is expected to" without a dated source, version, or release reference.

Fix:

- Compare quotes and numeric claims against the original source, not a secondary summary.
- Preserve exact names, titles, versions, and dates. If the source is ambiguous, say less.
- Replace relative dates with absolute dates or explicit version ranges.
- If roadmap timing is uncertain, scope the claim to the source date and avoid forward-looking promises.

## Rule: normalize repetitive style clusters without over-claiming

- Dense clusters of abstract "AI vocabulary": `pivotal`, `underscores`, `delve`, `interplay`, `intricate`, `tapestry`, `vibrant`, `landscape`, `showcase`, repeated sentence-openers like `Additionally,`.
- Rhetorical templates: `not only ... but also ...`, "it's not just X", rule-of-three lists, trailing synthesis clauses like "highlighting..." or "reflecting...".
- Presentation tells: emoji in headings, excessive bolding, title case where house style expects sentence case, overuse of em dashes, repetitive 3-column comparison tables, list bullets that restate the same sentence shape.
- Repeated sentence cadence: same clause order, same transition words, or every paragraph ending in a synthetic takeaway sentence.

Fix:

- Score clusters, not isolated words. Check genre, dialect, and translation context first.
- Flatten rhetorical flourishes into direct claims tied to evidence.
- Remove decorative readout structure when the table/list adds no decision value.
- Normalize punctuation, heading case, emphasis, and table/list style to the destination guide.

## Do not over-weight

- Detector scores, perfect grammar, "formal" tone, simple syntax, mixed English varieties, code-switching, curly quotes, one unusual word, or one conjunction pattern.
- Historical boilerplate such as "As an AI language model" and generic "In conclusion" can be stale but is not strong provenance evidence by itself.
- A file discussing AI detection may intentionally contain these strings.

## Recommended finding format

```text
Snippet:
Rule:
Why this is a quality issue:
Possible non-AI explanation:
Fix:
```

## Source basis

- Wikipedia: `https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing`
- Google style guide: `https://developers.google.com/style/tone`, `https://developers.google.com/style/excessive-claims`
- Citation fabrication studies: `https://pmc.ncbi.nlm.nih.gov/articles/PMC10484980/`, `https://pmc.ncbi.nlm.nih.gov/articles/PMC11153973/`
- Detector-bias and detector-fragility studies: `https://arxiv.org/abs/2304.02819`, `https://arxiv.org/abs/2303.11156`
- Time-drifting marker vocabulary: `https://arxiv.org/abs/2502.09606`
