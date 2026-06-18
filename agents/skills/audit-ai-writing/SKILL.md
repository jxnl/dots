---
name: audit-ai-writing
description: Audit pasted chatbot output, AI-cleanup diffs, wiki drafts, Markdown/MDX/docs, and source-backed articles for generic AI fluff, LLM writing tells, weak audience model, lack of theory of mind, inflated significance, vague attribution, leaked tokens, placeholders, broken markup, fabricated or mismatched citations, and detector false positives. Use for requests like "AI writing audit", "check for AI slop", "find writing fluff", "does this sound like ChatGPT", "cleanup LLM tells", "make this less generic", "verify these citations", "detector flagged this", or text containing turn0search0, oaicite, oai_citation, contentReference, utm_source=chatgpt.com, malformed references, or wrong target-format markup.
---

# AI Writing Audit

## Workflow

Open `patterns.md`, then review prose quality before citation mechanics unless the user specifically asks for citation verification:

1. Audience-model failures: prose that ignores what the reader knows, needs, doubts, or will do next; generic empathy; no real prioritization.
2. Fluff and LLM tells: inflated significance, vague stakes, template transitions, rhetorical balance, generic intros/outros, abstract filler, repeated cadence.
3. Claim quality: vague attribution, unsupported superlatives, stale timing, softened quantifiers, causal overreach.
4. Mechanical residue: leaked tool tokens, placeholders, broken markup, invalid references, wrong target-format syntax.
5. Citation support when relevant: real source, correct metadata, quote/page/number/date/name support, source-chaining mistakes.
6. Rewrite plan: smallest concrete fix, reader-specific framing, concrete verbs/nouns, target-format markup, and any verification still needed.

## Output

Lead with findings. For each finding, include:

- `Issue`
- `Evidence` (exact snippet or line location)
- `Class` (`P0`, `P1`, `P2`)
- `Why it matters`
- `Possible non-AI explanation`
- `Smallest fix`
- `Confidence` (`High`, `Medium`, `Low`, or `Needs source access`)
- `File/line` when available

Use classes this way:

- `P0`: fabricated or wrong source, materially unsupported claim, quote/number/name error, broken markup that changes meaning or publication viability.
- `P1`: recurring audience-model failure, generic claim scaffold, citation metadata drift, vague attribution, unsupported quantitative/date/causal claim.
- `P2`: isolated fluff, local style cleanup, minor formatting polish.

Return the top 5-8 findings. Merge repeated symptoms under one root cause. If the user asks for a rewrite, provide a compact replacement after the findings; otherwise give patch-ready guidance, not a full rewrite.

## Guardrails

- Do not infer AI authorship from detector scores, a single style cue, perfect grammar, formal tone, multilingual English, or translation artifacts.
- Treat suspicious markers as text-quality defects first. Name provenance risk only when objective residue or source failures justify it.
- Verify citation existence before judging claim support. If sources are unavailable, label the check as unverified and recommend the narrowest follow-up.
- Treat "lack of theory of mind" as an editorial diagnosis: the writing fails to model the reader, situation, objections, or next action. Do not use it as a claim about the writer.
- Do not moralize, shame the writer, or perform detector-score theater.
- Only patch files when the user asks for edits.

## Resource

- `patterns.md`: compact artifact taxonomy, verification checks, and rewrite guidance.
