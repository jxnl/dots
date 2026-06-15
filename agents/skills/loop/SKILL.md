---
name: loop
description: "Create and manage simple heartbeat automations attached to the current Codex thread. Use when Jason invokes $loop or asks this thread to keep going, check again, follow up, retry, monitor, or resume on a recurring cadence."
---

# Loop

Turn a plain-English request into a heartbeat on the current thread with as little ceremony as possible.

## Set Up The Loop

1. Infer the task from the request and current thread. Infer the stop condition when one is clear.
2. Decide whether a heartbeat is useful. Use one when the work benefits from returning to this thread after time passes or external state may change; continue immediately instead when the task can simply be finished now.
3. Use the requested cadence when sensible. Otherwise choose a cadence from the task's expected feedback latency, urgency, cost, and risk of noisy empty runs. Do not poll faster than the underlying state can plausibly change.
4. Choose a short verb-led name and a self-contained task prompt. Put the work, its completion condition, and this terminal behavior in the prompt:
   - when the completion condition is met, rename the current thread to `done: <short task name>` using the thread-title tool without inventing a thread ID;
   - report the completed result and stop the loop.
   Keep timing and thread-target details in the automation fields.
5. Call the automation tool with:
   - `mode=create`
   - `kind=heartbeat`
   - `destination=thread`
   - `status=ACTIVE`
   - the inferred `name`, `prompt`, and `rrule`
6. After creation succeeds, rename the current thread to `loop: <short task name>` using the thread-title tool without inventing a thread ID.
7. Return only the loop name, cadence, and what it will do.

Do not create a new thread, invent a thread ID, or substitute a detached cron job. Do not expose raw RRULE syntax to Jason.

## Use Judgment

- Ask when the task, cadence, stop condition, deadline, or notification behavior is materially ambiguous. Prefer the built-in user-question tool when it is available; otherwise ask one concise direct question.
- When asking about cadence, offer a small set of task-appropriate choices and recommend one. Do not make Jason translate the task into scheduling jargon.
- If the ambiguity is minor, make a reasonable assumption and state it instead of interrupting setup.
- Treat “loop,” “keep going,” and “check again” as authorization to create the heartbeat requested in that message.
- Preserve explicit deadlines, notification requirements, and stop conditions.
- Keep the lifecycle prefixes exact: `loop:` while active and `done:` after successful completion.
- Rename to `done:` only after successful completion, not after a failed run, pause, or temporary retry.
- Prefer updating an existing matching automation over creating a duplicate.
- For inspect, pause, resume, change, or delete requests, resolve the existing automation and use the corresponding automation-tool mode while preserving fields the user did not change. Restore the `loop:` title when resuming.
- If the automation tool is unavailable, say so plainly. Never emit a raw automation directive as a workaround.
