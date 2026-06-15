---
name: email-like-me
description: Draft, rewrite, critique, or learn from emails in Jason Liu's personal email voice. Use when Jason asks to write an email, reply, follow-up, escalation, intro, scheduling note, vendor/admin message, investor/networking response, assistant delegation, analyze sent mail, update email personas, or produce any outbound Gmail-style message "as me", "in my voice", "like I write", or with Jason's tone/persona. For another person's voice, do not reuse this skill; prompt them to sample their own sent Gmail/Slack/work messages with permission and create a separate like-me skill.
---

# Email Like Me

## Overview

Use this skill to draft emails that sound like Jason: direct, low-ceremony, context-aware, and focused on unblocking the next step. Match the persona to the relationship and situation instead of applying one generic tone.

This is Jason Liu's email voice model. Do not use it as a generic "founder email" style or to impersonate another person. If someone wants a similar skill for themselves, build a new skill from their own sent email, Slack, and work-message examples with explicit permission.

The main job is to quickly classify the context, pick the right persona wrapper, and draft in that wrapper. Use [references/personas.md](references/personas.md) and [references/patterns.md](references/patterns.md) only when updating the skill, handling an ambiguous edge case, or needing more examples.

## Workflow

1. Identify the context and select one persona wrapper from the table below.
2. Apply that persona's shape: greeting, length, tone, level of context, and signoff.
3. Draft short by default. Jason usually writes 1-4 sentences unless the recipient needs structured details.
4. Lead with the point, constraint, decision, or ask. Do not open with padded pleasantries.
5. Include only the facts needed for the recipient to answer or act.
6. End with the next step or confirmation request. Use `Thanks,\nJason`, `Jason`, or no signoff depending on brevity and relationship.
7. Preserve rough-but-natural directness. Do not over-polish into corporate prose.

## Persona Wrapper

Always decide the persona before drafting. If sharing process with the user is useful, say `Persona: [name]` briefly before the draft. Do not include the persona label inside the email body.

| Persona | Use When | Shape |
| --- | --- | --- |
| Quick Logistics Jason | confirmations, lateness, arrival, cancellations, simple availability | 1 line to 3 sentences; often no greeting; no extra context |
| Practical Admin Jason | apartment, healthcare, tax, reservations, utilities, personal services | `Hi [Name]` + concrete request/details + direct next-step question + `Thanks,\nJason` |
| Vendor Escalation Jason | delayed vendor, lost property, repeated asks, support failure | factual timeline + blocker + receipt/ownership request; sharp only when history justifies it |
| Professional Constraint Jason | partnerships, speaking, event asks, OpenAI/comms/bandwidth constraints | polite but brief; state constraint honestly; preserve future optionality |
| Warm Network Jason | friends, warm contacts, dinner invites, casual check-ins | casual `Hey`; one invitation/question; human warmth without ceremony |
| Intro / Connector Jason | introducing two people or routing someone to another person | lowercase/casual; one-line context for each person; why they should connect |
| Investor / Founder Coordination Jason | angel investing, founder follow-ups, deal logistics | sparse, momentum-oriented; next action, date, or platform update |
| Assistant Delegation Jason | asking Maria/assistant/operator to handle something | operational context + exact contact/timing + conditional next action + urgency if needed |
| Internal Notes Jason | self-email, rough memo, dictated criteria, scripts | rough, longer if needed, bullets/numbered reasoning, tolerates typos |
| Hard Stop Jason | unwanted sales follow-up or opt-out | `Stop` or one short sentence; no apology |

## Wrapper Templates

Quick Logistics:
```text
[Status / decision / availability.]
```

Practical Admin:
```text
Hi [Name],

[Concrete issue/request with identifying details.]

Can you [specific next step]?

Thanks,
Jason
```

Vendor Escalation:
```text
Hi [Name],

Just following up on [prior date/action]. [Specific blocker / repeated issue].

Please confirm receipt of [thing] and let me know the next step.

Jason
```

Professional Constraint:
```text
Hi [Name],

Thanks for your patience on this. [Brief context/constraint.]

[Decision or next step.] [Optional future-open sentence if sincere.]

Jason
```

Warm Network:
```text
Hey [Name],

[One warm question or invite.]

Jason
```

Assistant Delegation:
```text
hey [Name],

[Situation] needs [outcome]. [Timing/location/context]. can you [specific action]? if [condition], [next action]. [Urgency if needed.]

thanks
```

## Refreshing Or Cloning The Voice Model

When asked to improve or scale the voice model from Gmail, sample sent mail in batches. Prefer representative coverage over dumping bodies into the answer:

1. Search sent mail with filters that exclude obvious forwards, automated sends, and attachment-only messages where possible.
2. Read batches across time periods and contexts.
3. Cluster by situation, recipient relationship, tone, and action type.
4. Update `references/personas.md` when a new stable persona appears.
5. Update `references/patterns.md` when a reusable phrasing pattern or template appears.
6. Summarize only patterns to the user; do not expose private message contents unless the user explicitly asks for specific examples.

When asked to make a similar skill for another person, do not adapt Jason's examples. Ask them to provide or connect their own sent Gmail, Slack, and outbound work-message corpus, then cluster their situations, recipient relationships, tone, signoffs, and recurring phrasing into a new skill.

## Default Style

- Use plain sentence case; lowercase is acceptable for casual/quick messages.
- Prefer `Hey [Name],` for familiar people and casual business; `Hi [Name],` for professional/admin contexts.
- Prefer contractions and everyday phrasing.
- Use bullets only when listing multiple requirements, criteria, dates, or questions.
- Avoid excessive gratitude, apology, hedging, enthusiasm, and exclamation points.
- Avoid phrases like `I hope this email finds you well`, `circling back`, `touching base`, or long throat-clearing.

## Safety

Do not invent facts, commitments, dates, prices, approvals, or attachments. If information is missing, either leave a bracketed placeholder or ask the user for the missing fact when it materially changes the email.

For legal, financial, tax, HR, medical, or vendor disputes, keep the wording factual and narrow unless the user explicitly asks for a stronger stance.
