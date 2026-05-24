---
name: tweet-like-me
description: Use when Codex needs to draft, rewrite, critique, or generate Twitter/X posts and replies in Jason Liu's personal Twitter voice, including persona-specific variants for Codex/product commentary, feedback asks, launch notes, quote-tweet reactions, casual replies, and operator/value takes.
---

# Tweet Like Me

## Workflow

Use this skill to turn an idea, rough draft, reply context, or screenshot summary into tweets that sound like Jason.

1. Identify the task: draft, rewrite, reply, critique, or variants.
2. Read `references/style-guide.md` for the core voice.
3. Read `references/personas.md` and choose the persona that fits the situation. If the user asks for persona grouping or does not specify a persona, produce variants across the most relevant personas.
4. Read `references/examples.md` when you need concrete shapes or transformations.
5. Output 3-5 concise variants by default, labeled by persona and vibe.

## Defaults

- Ask a follow-up only when the topic, audience, or reply context is too vague to draft responsibly.
- Preserve user-supplied facts. Do not invent personal experiences, internal company facts, product promises, release dates, or claims about OpenAI.
- Prefer short, concrete tweets over polished threads. Write a thread only when the user asks.
- Include rationale only for critique, ranking, or when the user asks why a draft works.
- For rewrites, keep the user's intended point unless they ask for sharper positioning.
- For replies, match the conversational stakes: short acknowledgement, useful question, offer to help, or gentle joke.

## Output Shape

When drafting variants, use:

```text
codex-teacher / practical:
...

customer-reply-guy / helpful:
...

casual-reactor / low effort:
...
```

When critiquing, use:

```text
Verdict: ...

What sounds like you:
- ...

What to fix:
- ...

Rewrite:
...
```
