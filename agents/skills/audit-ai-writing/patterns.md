# AI Writing Patterns and Fixes

Compact checklist for AI-shaped writing fluff, LLM tells, audience-model failures, markup residue, citation failures, and practical rewrites. Use it to improve the text, not to prove authorship.

## Evidence ladder

Prefer high-signal editorial defects before detector-style speculation:

1. **Audience-model failures**: no sense of what the reader knows, cares about, doubts, or needs next.
2. **Fluff and LLM tells**: generic significance, rhetorical balance, template transitions, abstract filler, repeated cadence.
3. **Document-shape failures**: formula sections, unsupported roadmap language, stale relative time, broken cross-references.
4. **Machine residue**: leaked tool tokens, placeholders, tracking params, malformed or wrong-format markup.
5. **Citation failures**: source cannot be found, identifier resolves elsewhere, metadata is wrong, or the source does not support the claim.

Machine residue and citation failures can justify strong provenance concern. Fluff, LLM tells, and audience-model failures justify rewrite guidance, not authorship claims.

## Review order

1. Identify where the text fails to model the reader: audience, stakes, objections, decision point, or next action.
2. Cut generic openings, conclusions, significance claims, rhetorical balance, and abstract filler.
3. Replace vague or overconfident prose with concrete actors, actions, constraints, examples, dates, and consequences.
4. Normalize repeated cadence, transition words, table/list shape, and house-style drift.
5. Remove leaked tokens, placeholders, malformed markup, and broken internal references.
6. Verify cited sources when claims, quotes, numbers, dates, or names matter.

## Rule: find audience-model failures and weak theory of mind

Treat "lack of theory of mind" as a text problem: the prose does not appear to understand the reader's context, not as a psychological claim about the writer.

Signals:

- Starts broad instead of answering the reader's likely question.
- Explains obvious context while skipping the decision-relevant detail.
- Uses generic reassurance or empathy without naming the user's actual constraint, risk, objection, or tradeoff.
- Gives balanced-sounding pros/cons without ranking them for the situation.
- Ends with a synthetic takeaway that does not change what the reader should believe or do.
- Uses "important", "critical", "significant", or "valuable" without saying important to whom, for what decision, by what evidence.
- Treats all audiences the same: beginner and expert, buyer and maintainer, patient and clinician, internal team and public reader.
- Makes a claim that is technically plausible but pragmatically unhelpful because it ignores timing, incentives, cost, risk, authority, or implementation context.

Fix:

- Name the reader's job-to-be-done, decision, objection, or constraint in plain terms.
- Lead with the specific answer or consequence before background.
- Replace "this is important" with "this matters because [specific reader] must decide/do/avoid [specific thing]."
- Rank tradeoffs. Say which factor dominates and under what condition.
- Cut generic empathy; keep only context that changes the recommendation or rewrite.
- Add one concrete example, counterexample, or edge case when it reveals judgment.

## Rule: remove machine residue and format/schema hallucinations first

Machine residue:

- Leaked tool/citation tokens: `turn0search0`, `turn0image0`, `turn0news0`, `turn0file0`, `oaicite`, `oai_citation`, `contentReference[...]`, `attributableIndex`, `generated-reference-identifier`, `[attached_file:1]`, `[web:1]`, `grok_card`, `grok-card`, stray `+1`.
- Private-use citation glyphs rendered as odd symbols, including wrapped `\ue200...\ue202` markers.
- Placeholder values: `INSERT_SOURCE_URL`, `URL_HERE`, `PASTE_*_URL_HERE`, `2025-XX-XX`, bracketed drafting instructions.
- Chatbot copy/paste leftovers: `As an AI language model...`, `I hope this helps`, `Would you like me to...`, `Sure, here...`, `Certainly...`, `Below is...`, "copy and paste this", orphaned `Subject:`, orphaned `Draft:` / `Response:`.
- Tracking params from copied chatbot links: `utm_source=chatgpt.com`, `utm_source=openai`, `utm_source=copilot.com`, `referrer=grok.com`.

Format/schema hallucinations:

- Wrong markup for the destination format: Markdown headings/bold/links in MediaWiki text, raw HTML where disallowed, fenced code wrappers around prose, skipped heading levels, duplicate anchors.
- Invalid or hallucinated wiki structures: non-existent templates/categories, pre-placed maintenance templates, AfC "submission statement" residue, unused named references dumped into a references section.
- Broken Markdown references: undefined reference labels, unused reference definitions, empty links, invalid fragment IDs.
- Broken internal references: links to headings/files that do not exist, invented section names, or "see above/below" pointers that no longer match the document structure.

Citation integrity failures:

- Nonexistent source, fake article/chapter title, or real venue/publisher with invented metadata.
- Valid DOI/PMID/ISBN that resolves to a different work than the citation text.
- Partly real citation with corrupted author, title, journal, volume, page, date, DOI, ISBN, or URL.
- Link text and hyperlink target point to different works.
- In-text citation has no bibliography entry, or bibliography entries are never cited in the body.
- Book or chapter citation lacks page numbers for a specific claim.
- Quoted text, speaker names, or publication dates do not match the cited source.
- Round statistics or precise percentages appear without a source that actually states that number.

Fix:

- Delete residue and placeholder text. Replace with verified citations or remove the claim.
- Convert markup to the target format and run deterministic link/render checks if available.
- For citations, verify the object first: title, authors, date, venue, identifier, and URL. Then verify claim support in the cited text.
- For high-impact claims, confirm direct claim support before keeping the text. Use 2-3 authoritative sources when the claim is contentious, current, medical/legal/financial, or biographical.
- Do not label a reference "hallucinated" until you rule out a dead link, archive drift, or a minor citation typo.

## Rule: rewrite unsupported prose, vague attribution, and template structure

- Generic scene-setting intros: "In today's fast-paced world...", "In an era where...", "This article explores...", "Let's dive in...".
- Generic significance language: "marked a pivotal moment", "underscores its significance", "enduring legacy", "broader landscape", rhetorical `serves as` / `stands as`.
- Weasel attribution: "experts argue", "observers note", "some critics say", "several publications", "independent coverage" as body prose.
- Knowledge-gap boilerplate and speculation: "As of my last knowledge update", "Based on available information", "Specific details are limited", "likely supports", "keeps a low profile".
- Formula sections with weak sourcing: "Despite these challenges...", "Future Outlook", generic conclusions that restate themes without new evidence.
- Overstated or unverifiable claims: "best", "fastest", "revolutionary", "guarantees", broad security or performance assertions with no cited data.
- Citation drift: source exists, but author/title/date/page/version was silently normalized, paraphrased, or rounded enough that retrieval or attribution becomes wrong.
- Over-balanced filler: "on one hand / on the other hand", "while there are many factors", or broad caveats that avoid making a checkable claim.
- Causal overreach: "led to", "drove", "enabled", "therefore", "as a result" when the source only supports sequence, correlation, or opinion.
- Softened unsourced quantification: "many", "numerous", "a wide range of", "substantial", "significant" with no count, timeframe, or denominator.
- Synthetic summary clauses: sentence tails like "highlighting its importance", "reflecting broader trends", "showcasing the potential", or "underscoring the need" that add mood but no evidence.
- Reader-agnostic advice: "consider your needs", "it depends on your goals", "choose what works best" without naming the actual variables that should decide.

Fix:

- Replace abstract praise with who/what/when/where and the exact source passage that supports the claim.
- Name the source or remove the attribution. Do not imply consensus from one weak source.
- Cut speculation and state only what is verified. Use absolute dates or versioned scope when timing matters.
- Fold real constraints into topical sections and delete empty "future/challenges" filler.
- Delete generic intro/outro scaffolding and start with the concrete subject, claim, and evidence.
- Downgrade causal verbs to neutral chronology unless a source explicitly supports causation.
- Replace vague volume claims with exact counts, dates, and denominators, or remove them.
- Write one idea per sentence where possible, put the actor near the front, define jargon once, and avoid filler such as "please note", "at this time", "simply", and "quickly".
- Replace reader-agnostic advice with a decision rule: "Choose X if A; choose Y if B."

## Rule: verify quotes, numbers, names, and dates exactly

- Quotes that sound polished but do not match the source text verbatim, or quote punctuation/ellipsis that changes meaning.
- Speaker/title drift: person names, company names, venue names, paper titles, and API or product names are close but not exact.
- Number drift: rounded metrics, percentages, rankings, and date ranges copied into bullets or tables but not stated that way in the source.
- Vague time anchors in durable docs: "recently", "currently", "today", "now", "in recent years", "soon".
- Unsupported roadmap language: "planned", "upcoming", "will support", "is expected to" without a dated source, version, or release reference.
- Source-chaining errors: a secondary source cites a primary source, but the prose attributes the claim to the wrong source or upgrades a report/opinion into fact.

Fix:

- Compare quotes and numeric claims against the original source, not a secondary summary.
- Preserve exact names, titles, versions, and dates. If the source is ambiguous, say less.
- Replace relative dates with absolute dates or explicit version ranges.
- If roadmap timing is uncertain, scope the claim to the source date and avoid forward-looking promises.
- Keep the citation attached to the sentence it supports. Split sentences when one citation supports only part of a compound claim.
- Treat generated bibliographies as untrusted until checked against a scholarly index, publisher page, archive copy, or primary source.

## Rule: normalize repetitive style clusters without over-claiming

- Dense clusters of abstract "AI vocabulary": `pivotal`, `underscores`, `delve`, `interplay`, `intricate`, `tapestry`, `vibrant`, `landscape`, `showcase`, repeated sentence-openers like `Additionally,`.
- Rhetorical templates: `not only ... but also ...`, "it's not just X", rule-of-three lists, trailing synthesis clauses like "highlighting..." or "reflecting...".
- Presentation tells: emoji in headings, excessive bolding, title case where house style expects sentence case, overuse of em dashes, repetitive 3-column comparison tables, list bullets that restate the same sentence shape.
- Repeated sentence cadence: same clause order, same transition words, or every paragraph ending in a synthetic takeaway sentence.

Fix:

- Weigh clusters, not isolated words. Check genre, dialect, translation context, and house style first.
- Flatten rhetorical flourishes into direct claims tied to evidence.
- Remove decorative readout structure when the table/list adds no decision value.
- Normalize punctuation, heading case, emphasis, and table/list style to the destination guide.

## Do not over-weight

- Detector scores, perfect grammar, "formal" tone, simple syntax, mixed English varieties, code-switching, curly quotes, one unusual word, or one conjunction pattern.
- Historical boilerplate such as "As an AI language model" and generic "In conclusion" can be stale but is not strong provenance evidence by itself.
- A file discussing AI detection may intentionally contain these strings.
- Words known as AI markers drift over time as writers and models adapt. Do not build a finding around one vocabulary item.

## Recommended finding format

```text
Snippet:
Rule:
Why this is a quality issue:
Possible non-AI explanation:
Fix:
Confidence:
```

## Source basis

- Wikipedia: `https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing`
- Google style guide: `https://developers.google.com/style/tone`, `https://developers.google.com/style/excessive-claims`
- Citation fabrication studies: `https://pmc.ncbi.nlm.nih.gov/articles/PMC10484980/`, `https://pmc.ncbi.nlm.nih.gov/articles/PMC11153973/`
- Detector-bias and detector-fragility studies: `https://arxiv.org/abs/2304.02819`, `https://arxiv.org/abs/2303.11156`
- Time-drifting marker vocabulary: `https://arxiv.org/abs/2502.09606`
- Large-scale and retrieval-grounded citation audits: `https://arxiv.org/abs/2605.07723`, `https://arxiv.org/abs/2605.27700`, `https://arxiv.org/abs/2603.03299`, `https://arxiv.org/abs/2503.19848`
