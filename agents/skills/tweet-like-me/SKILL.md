---
name: tweet-like-me
description: Use when Codex needs to write, rewrite, critique, or reply on Twitter/X in Jason Liu's personal voice. Trigger for requests like "tweet like me", "write this in my style", "make this sound like Jason", "draft a reply", or when Jason asks for Twitter copy about Codex, product building, feedback, launches, quote-tweets, or operator/value takes.
---

# Tweet Like Me

Use this skill to write tweets that sound like Jason without asking the user to pick a persona. Infer the right voice from the task, context, and audience. Produce variants only when the user explicitly asks for variants, options, or comparison.

Source: latest 400 `@jxnlco` tweets fetched on 2026-05-24. The corpus was roughly half original posts and half replies, with many short reactions, Codex/product posts, practical asks, and live dogfooding notes.

## Default Workflow

1. Identify the job: new tweet, rewrite, reply, quote-tweet, critique, thread, or feedback ask.
2. Pick the single best-fit voice from the task:
   - teaching a workflow -> `codex-teacher`
   - live demo/dogfooding -> `builder-in-public`
   - replying to a user -> `customer-reply-guy`
   - asking for product feedback -> `feedback-collector`
   - reacting to a link/demo -> `casual-reactor`
   - making a taste/shipping/company-motion point -> `operator-values`
   - mentioning OpenAI/Codex/team/model internals -> `inside-baseball`
3. Draft one strong answer by default. If the user asks for options, give 3-5 labeled variants.
4. Ask a follow-up only when the topic, audience, or reply context is too vague to draft responsibly.

## Core Voice

- Casual, direct, present-tense, and product-native.
- Sounds like a builder watching the thing happen in real time, not a marketer announcing a feature.
- Mix practical usefulness with low-friction internet speech.
- Start close to the thought. Skip throat-clearing.
- Prefer short, concrete tweets over polished threads.
- Let specificity carry credibility: product names, workflows, commands, UI surfaces, models, teams, and user situations.
- Keep some roughness when it fits: lowercase starts, fragments, abrupt reactions, sparse punctuation.
- Use line breaks for emphasis in higher-stakes posts.

Corpus fingerprint:

- Median length around 56 characters; mean around 75.
- Most posts are one-liners; longer posts use blank lines between short thoughts.
- Many replies are one sentence or less.
- Links often appear with only a short reaction.
- Questions show up mostly when collecting feedback.
- Common language: `codex`, `app`, `use`, `new`, `openai`, `chatgpt`, `computer`, `team`, `ask`, `goal`, `try`, `dm me`, `let me know`, `what do you need from us`.

## Voice Modes

Use these as internal modes, not as a menu the user has to choose.

### `codex-teacher`

Use for tips, workflows, practical "try this" posts, feature discovery, and helping people use Codex better.

- Shape: "If you're using...", "try asking...", "codex tip N: ...".
- Include concrete commands, UI surfaces, or actions when available.
- End with a practical payoff, not a grand claim.

Example shape:

```text
codex tip: skills

if codex is open right now just ask it what skills you should install

weirdly effective way to make the app feel more yours
```

### `builder-in-public`

Use for live product observations, dogfooding, demos, screenshots, and build logs.

- Shape: "Codex is currently...", "Watching codex...", "I just had..."
- Include weird concrete details that make it feel witnessed.
- Keep amazement matter-of-fact.

Example shape:

```text
Watching codex create workers from the cloudflare dashboard.
```

### `customer-reply-guy`

Use for replies to users, issue reports, requests, complaints, and people building on Codex.

- Keep most replies under one sentence.
- Ask one useful follow-up if needed.
- Offer help without overpromising.
- Common replies: `dm me`, `noted`, `what do you need from us`, `Can you send the transcript?`

### `feedback-collector`

Use for asking users what is missing, what hurts, or what should be better.

- Invite detail: examples, transcripts, workflows, screenshots.
- Promise only reasonable handling, like summarizing or sharing internally, if that is supplied or safe.

Example shape:

```text
If you're using codex desktop app today, what features still feel missing?

Let me know and I'll summarize the feedback.
```

### `casual-reactor`

Use for quote-tweet style reactions, link reactions, jokes, and quick social replies.

- Keep it tiny when the context carries the point.
- Common shapes: `Wow`, `Lmfao`, `:O`, `thnx`, `big if true`, `so slay`.
- Do not force explanation. The shortness is often the bit.

### `operator-values`

Use for short takes about taste, shipping, audience, selfless building, growth, company motion, and what matters.

- One strong claim plus one clarifying sentence.
- Blunt, values-forward, sometimes tender.
- Avoid management-consulting language.
- Let the take be personal and concrete, not universal law.

Example shape:

```text
Who cares.

You gotta make things cause it's important for the audience to see them.

It's supposed to be a selfless act.
```

### `inside-baseball`

Use for OpenAI/Codex/team references, model comparisons, launches, limits, and internal-sounding context.

- Only use facts provided by the user or public context already in the prompt.
- Never invent internal claims, team decisions, timelines, roadmap promises, or private experiences.
- Good grounded language: `codex team`, `OpenAI`, `5.5`, `xhigh`, `pro`, `skills`, `app shots`, `remote computer use`.

## Avoid

- Do not sound like SaaS marketing: no "unlock your potential", "game changer", or polished launch-copy cadence.
- Do not over-explain. Most drafts should be shorter than the average assistant instinct.
- Do not add hashtags unless the user explicitly asks.
- Do not add emoji unless the source context already uses one or the user asks.
- Do not invent personal experiences, internal company facts, product promises, release dates, or claims about OpenAI.
- Do not make every tweet funny. Many are useful, direct, or observational.
- Do not label the voice mode unless the user asks for variants or critique.

## Output Rules

- For a normal draft/rewrite: return the tweet only.
- For a reply: return the reply only.
- For critique: give a short verdict, 1-3 fixes, then a rewrite.
- For requested variants: give 3-5 options labeled by voice mode and vibe.
- For threads: keep each tweet short and numbered only if the user asks for numbering.
